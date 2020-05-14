from typing import List, Optional, Tuple

import numpy as np



# noinspection PyPep8Naming


class EM:
    _state_dim: int
    _observation_dim: int
    _no_sequences: int

    _T: int
    _y: np.ndarray
    _yy: np.ndarray

    _x_hat: np.ndarray

    _A: np.ndarray
    _Q: np.ndarray

    _C: np.ndarray
    _R: np.ndarray

    _m0: np.ndarray
    _V0: np.ndarray

    _self_correlation: List[np.ndarray]
    _cross_correlation: List[np.ndarray]

    _marginal_kalman_likelihood: float

    _Q_problem: bool
    _C_problem: bool
    _V0_problem: bool

    _checkpoint: Optional[Tuple]


    def __init__(self, state_dim: int, y: List[List[np.ndarray]]):
        self._state_dim = state_dim
        self._observation_dim = y[0][0].shape[0]
        self._no_sequences = len(y)

        # Number of time steps, i.e. number of output vectors.
        self._T = len(y[0])
        # Output vectors.
        # Normalize the measurements around the mean.
        y = np.array(y) - np.ones((self._no_sequences, self._T, 1)) @ np.mean(y, axis = (0, 1)).reshape(1, -1)
        self._y = np.transpose(y, axes = (0, 2, 1))  # from [sequence, T, dim] to [sequence, dim, T]

        # Sum of the diagonal entries of the outer products y @ y.T.
        self._yy = np.sum(np.multiply(self._y, self._y), axis = (0, 2)).flatten() / (self._T * self._no_sequences)

        # State dynamics matrix.
        self._A = np.eye(self._state_dim)
        # State noise covariance.
        self._Q = np.eye(self._state_dim)

        # Output matrix.
        self._C = np.eye(self._observation_dim, self._state_dim)
        # Output noise covariance.
        self._R = np.ones(self._observation_dim)

        # Initial state mean.
        self._m0 = np.ones((self._state_dim, 1))
        # Initial state covariance.
        self._V0 = np.eye(self._state_dim)

        # The marginal log-likelihood of the Kalman filter used for convergence checking.
        self._marginal_kalman_likelihood = 0.0

        # Metrics for sanity checks.
        self._Q_problem: bool = False
        self._R_problem: bool = False
        self._V0_problem: bool = False

        self._checkpoint = None


    def fit(self, precision = 0.00001) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, List[float], bool, bool, bool]:
        history = []
        likelihood_base = 0
        iteration = 0
        previous_marginal_kalman_likelihood = None
        while True:
            self.e_step()
            self.m_step()

            marginal_kalman_likelihood = self.get_marginal_kalman_likelihood()
            likelihood = self.get_likelihood()
            history.append(likelihood)
            print('Iter. %5d; Likelihood: %15.5f' % (iteration, likelihood))

            if iteration > 0 and likelihood < history[-2]:
                print('Likelihood violation! New likelihood is higher than previous.')

            if iteration < 2:
                # Typically the first iteration of the EM-algorithm is far off, so set the likelihood base on the second iteration.
                likelihood_base = marginal_kalman_likelihood
            elif (marginal_kalman_likelihood - likelihood_base) < (1 + precision) * (previous_marginal_kalman_likelihood - likelihood_base):
                print('Converged! :)')
                break

            previous_marginal_kalman_likelihood = marginal_kalman_likelihood
            iteration += 1

        # noinspection PyTypeChecker
        return *self.get_estimations(), history, *self.get_problems()


    def e_step(self) -> None:
        #
        # Forward pass.

        P: List[Optional[np.ndarray]] = [None] * self._T
        V: List[Optional[np.ndarray]] = [None] * self._T
        m = np.zeros((self._no_sequences, self._state_dim, self._T))
        K = np.zeros((self._state_dim, self._observation_dim))

        marginal_kalman_likelihood = 0.0
        for t in range(0, self._T):
            if t == 0:
                # Initialization.
                m_pre = self._m0.T
                P_pre = self._V0
            else:
                m_pre = m[:, :, t - 1] @ self._A.T
                P_pre = self._A @ V[t - 1] @ self._A.T + self._Q
                P[t - 1] = P_pre

            innovation_cov = self._C @ P_pre @ self._C.T + np.diag(self._R)
            K = P_pre @ self._C.T @ np.linalg.inv(innovation_cov)
            y_diff = self._y[:, :, t] - m_pre @ self._C.T
            m[:, :, t] = m_pre + y_diff @ K.T
            V[t] = P_pre - K @ self._C @ P_pre

            # Calculate marginal log-likelihood of the Kalman filter using the measurement pre-fit residual and the pre-fit residual covariance.
            # See https://en.wikipedia.org/wiki/Kalman_filter#Marginal_likelihood for more information.
            detP = np.linalg.det(innovation_cov)
            if detP > 0:
                marginal_kalman_likelihood += - self._no_sequences * np.log(detP) / 2 \
                                              - np.sum(np.sum(np.multiply(y_diff, y_diff @ np.linalg.inv(innovation_cov)), axis = 0), axis = 0) / 2

        # See a few lines above about what is calculated here.
        self._marginal_kalman_likelihood = marginal_kalman_likelihood - self._no_sequences * self._T * self._observation_dim * np.log(2 * np.pi) / 2

        #
        # Backward Pass.

        V_hat: List[Optional[np.ndarray]] = [None] * self._T
        J: List[Optional[np.ndarray]] = [None] * self._T
        m_hat = np.zeros((self._no_sequences, self._state_dim, self._T))
        self_correlation = []
        cross_correlation = []

        t = self._T - 1
        m_hat[:, :, t] = m[:, :, t]
        V_hat[t] = V[t]
        self_correlation.append(V_hat[t] + m_hat[:, :, t].T @ m_hat[:, :, t] / self._no_sequences)
        for t in reversed(range(1, self._T)):
            # J[t - 1] = V[t - 1] @ self._A.T @ np.linalg.inv(P[t - 1])
            J[t - 1] = np.linalg.solve(P[t - 1], self._A @ V[t - 1].T).T
            m_hat[:, :, t - 1] = m[:, :, t - 1] + (m_hat[:, :, t] - m[:, :, t - 1] @ self._A.T) @ J[t - 1].T
            V_hat[t - 1] = V[t - 1] + J[t - 1] @ (V_hat[t] - P[t - 1]) @ J[t - 1].T

            self_correlation.append(V_hat[t - 1] + m_hat[:, :, t - 1].T @ m_hat[:, :, t - 1] / self._no_sequences)
            # cross_correlation.append(J[t - 1] @ V_hat[t] + m_hat[:, :, t].T @ m_hat[:, :, t - 1] / self._no_sequences)

        # Compute cross-correlation according to Ghahramani (the calculation reported by Minka seems to be less stable).
        for t in reversed(range(1, self._T)):
            if t == self._T - 1:
                # Initialization.
                P_cov = self._A @ V[t - 1] - K @ self._C @ self._A @ V[t - 1]
            else:
                # noinspection PyUnboundLocalVariable
                P_cov = V[t] @ J[t - 1].T + J[t] @ (P_cov - self._A @ V[t]) @ J[t - 1].T

            cross_correlation.append(P_cov + m_hat[:, :, t].T @ m_hat[:, :, t - 1] / self._no_sequences)

        self._x_hat = m_hat
        self._self_correlation = list(reversed(self_correlation))
        self._cross_correlation = list(reversed(cross_correlation))


    def m_step(self) -> None:
        yx_sum = np.sum([self._y[:, :, t].T @ self._x_hat[:, :, t] for t in range(self._T)], axis = 0)
        self_correlation_sum = np.sum(self._self_correlation, axis = 0)
        cross_correlation_sum = np.sum(self._cross_correlation, axis = 0)

        self._C = np.linalg.solve(self_correlation_sum, yx_sum.T).T / self._no_sequences
        self._R = self._yy - np.diag(self._C @ yx_sum.T) / (self._T * self._no_sequences)
        # Do not subtract self._cross_correlation[0] here as there is no cross correlation \( P_{ 0, -1 } \) and thus it is not included in the list nor the sum.
        self._A = np.linalg.solve(self_correlation_sum - self._self_correlation[-1], cross_correlation_sum.T).T
        self._Q = np.diag(np.diag(self_correlation_sum - self._self_correlation[0] - self._A @ cross_correlation_sum.T)) / (self._T - 1)
        self._m0 = np.mean(self._x_hat[:, :, 0], axis = 0).reshape(-1, 1)
        outer_part = self._x_hat[:, :, 0] - np.ones((self._no_sequences, 1)) @ self._m0.T
        self._V0 = self._self_correlation[0] - np.outer(self._m0, self._m0) + outer_part.T @ outer_part / self._no_sequences

        self._Q_problem = np.linalg.det(self._Q) <= 0
        self._R_problem = np.linalg.det(np.diag(self._R)) <= 0
        self._V0_problem = np.linalg.det(self._V0) <= 0

        if self._Q_problem:
            print('Q problem!')
        if self._R_problem:
            print('R problem!')
        if self._V0_problem:
            print('V0 problem!')


    def checkpoint(self):
        self._checkpoint = (self._x_hat, self._A, self._Q, self._C, self._R, self._m0, self._V0, self._self_correlation, self._cross_correlation,
                            self._marginal_kalman_likelihood, self._Q_problem, self._R_problem, self._V0_problem)


    def rollback(self):
        if self._checkpoint is None:
            raise Exception('No checkpoint set; cannot rollback!')

        (self._x_hat, self._A, self._Q, self._C, self._R, self._m0, self._V0, self._self_correlation, self._cross_correlation,
         self._marginal_kalman_likelihood, self._Q_problem, self._R_problem, self._V0_problem) = self._checkpoint


    def get_estimations(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        return self._A, self._Q, self._C, self._R, self._m0, self._V0


    def get_likelihood(self) -> float:
        # Store some variables to make the code below more readable.
        N = self._no_sequences
        p = self._observation_dim
        k = self._state_dim
        T = self._T
        A = self._A
        Q = self._Q
        C = self._C
        m0 = self._m0
        V0 = self._V0
        y = self._y
        x_hat = self._x_hat
        R = np.diag(self._R)

        return 0.5 * (- np.sum([(y[:, :, t] - x_hat[:, :, t] @ C.T) @ np.linalg.inv(R) @ (y[:, :, t] - x_hat[:, :, t] @ C.T).T for t in range(0, T)]) / N
                      - N * T * np.log(np.linalg.det(R))
                      - np.sum([(x_hat[:, :, t] - x_hat[:, :, t - 1] @ A.T) @ np.linalg.inv(Q) @ (x_hat[:, :, t] - x_hat[:, :, t - 1] @ A.T).T for t in range(1, T)]) / N
                      - N * (T - 1) * np.log(np.linalg.det(Q))
                      - np.sum((x_hat[:, :, 0] - m0.T) @ np.linalg.inv(V0) @ (x_hat[:, :, 0] - m0.T).T)
                      - N * np.log(np.linalg.det(V0))
                      - N * T * (p + k) * np.log(2 * np.pi))


    def get_marginal_kalman_likelihood(self) -> float:
        return self._marginal_kalman_likelihood


    def get_problems(self) -> Tuple[bool, bool, bool]:
        return self._Q_problem, self._R_problem, self._V0_problem
