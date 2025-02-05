import os
from typing import Final, List, Optional

import numpy as np

from investigation import util
from investigation.observations import compute_observations
from investigation.plot_util import figsize, show_debug_info, SubplotsAndSave
from investigation.util import ExperimentConfig, ExperimentResult
from src.rollout import compute_rollout

PLOT_CONFIDENCE: Final[bool] = os.environ.get('OMIT_CONFIDENCE') is None
PLOT_ROLLOUT: Final[bool] = os.environ.get('OMIT_ROLLOUT') is None
PLOT_WITHOUT_CONTROL: Final[bool] = os.environ.get('OMIT_WITHOUT_CONTROL') is None


def plot_rollout(out_dir: str, config: ExperimentConfig, result: ExperimentResult, plot_latents: bool, plot_observations: bool, plot_lunar_lander: bool):
    if not plot_latents and not plot_observations:
        return

    N = min(config.N, 10)
    (latent_rollouts, latent_covs), (obs_rollouts, obs_covs), without_control = compute_rollout(config, result, N)
    latent_rollouts_without_control = [None if without_control is None else without_control[0]] * N
    obs_rollouts_without_control = [None if without_control is None else without_control[1]] * N
    obs_covs_without_control = [None if without_control is None else without_control[2]] * N

    latent_pred_rollouts, latent_pred_covs, obs_pred_rollouts, obs_pred_covs = [], [], [], []
    for n in range(N):
        (latent_pred_rollout, latent_pred_cov), (obs_pred_rollout, obs_pred_cov), _ = compute_rollout(config, result, 1,
                                                                                                      initial_value=result.estimations_latents[n, :, -1],
                                                                                                      initial_cov=result.V_hat[n, :, :, -1],
                                                                                                      T=config.T - config.T_train + 1,
                                                                                                      do_control=False)
        latent_pred_rollouts.append(latent_pred_rollout[0])
        latent_pred_covs.append(latent_pred_cov[0])
        obs_pred_rollouts.append(obs_pred_rollout[0])
        obs_pred_covs.append(obs_pred_cov[0])

    if plot_latents:
        _plot_latent_rollout(out_dir, config, result, N, latent_rollouts, latent_covs, latent_rollouts_without_control, latent_pred_rollouts, latent_pred_covs)
    if plot_observations:
        _plot_observations_rollout(out_dir, config, result, N, obs_rollouts, obs_covs, obs_rollouts_without_control, obs_covs_without_control, obs_pred_rollouts, obs_pred_covs)
    if plot_lunar_lander:
        _plot_lunar_lander(out_dir, config, result, N, obs_rollouts)


def _plot_latent_rollout(out_dir: str, config: ExperimentConfig, result: ExperimentResult, N: int, latent_rollout: List[np.ndarray], latent_covariances: List[np.ndarray],
                         latent_rollout_without_control: List[Optional[np.ndarray]], latent_pred_rollout: List[np.ndarray], latent_pred_covariances: List[np.ndarray]):
    domain = np.arange(config.T) * config.h
    domain_train = domain[:config.T_train]
    domain_test = domain[config.T_train - 1:]

    for dim in range(config.latent_dim):
        for n, item in enumerate(
                zip(latent_rollout[:N], latent_covariances[:N], latent_rollout_without_control[:N], result.estimations_latents[:N], latent_pred_rollout[:N],
                    latent_pred_covariances[:N])):
            latent_trajectory, latent_covariance, latent_trajectory_without_control, latent_trajectory_smoothed, latent_pred_trajectory, latent_pred_covariance = item
            with SubplotsAndSave(out_dir, f'rollout-latents-N{n}-D{dim}', place_legend_outside=True) as (fig, ax):
                show_debug_info(fig, config, result)

                _plot_latent_rollout_to_ax(ax, config, dim, domain, domain_test, domain_train, latent_covariance, latent_pred_covariance, latent_pred_trajectory, latent_trajectory,
                                           latent_trajectory_smoothed, latent_trajectory_without_control, n, result)

                if N > 1:
                    ax.set_title('Sequence %d' % (n + 1))
                ax.set_xlabel('$t$')

    for n, item in enumerate(
            zip(latent_rollout[:N], latent_covariances[:N], latent_rollout_without_control[:N], result.estimations_latents[:N], latent_pred_rollout[:N],
                latent_pred_covariances[:N])):
        latent_trajectory, latent_covariance, latent_trajectory_without_control, latent_trajectory_smoothed, latent_pred_trajectory, latent_pred_covariance = item
        ncols, nrows, check = 1, None, 0
        while nrows is None or nrows > ncols + check:
            ncols += 1
            nrows = int(np.ceil(config.latent_dim / ncols))
            check += 1
        with SubplotsAndSave(out_dir, f'rollout-latents-N{n}',
                             nrows=nrows,
                             ncols=ncols,
                             place_legend_outside=True,
                             sharex='col',
                             squeeze=False) as (fig, axs):
            show_debug_info(fig, config, result)
            for dim, ax in zip(range(config.latent_dim), axs.flatten()):
                _plot_latent_rollout_to_ax(ax, config, dim, domain, domain_test, domain_train, latent_covariance, latent_pred_covariance, latent_pred_trajectory, latent_trajectory,
                                           latent_trajectory_smoothed, latent_trajectory_without_control, n, result)

                if N > 1:
                    ax.set_title('Sequence %d' % (n + 1))
                if dim == config.latent_dim - 1 or dim == config.latent_dim - 2:
                    ax.set_xlabel('$t$')


def _plot_latent_rollout_to_ax(ax, config, dim, domain, domain_test, domain_train, latent_covariance, latent_pred_covariance, latent_pred_trajectory, latent_trajectory,
                               latent_trajectory_smoothed, latent_trajectory_without_control, n, result):
    latent_trajectory_train = latent_trajectory[:config.T_train, dim]
    latent_trajectory_test = latent_trajectory[config.T_train - 1:, dim]
    # Rollout w/o control inputs.
    if PLOT_WITHOUT_CONTROL and PLOT_ROLLOUT and latent_trajectory_without_control is not None:
        latent_trajectory_without_control_train = latent_trajectory_without_control[:config.T_train, dim]
        latent_trajectory_without_control_test = latent_trajectory_without_control[config.T_train - 1:, dim]

        ax.plot(domain_train, latent_trajectory_without_control_train, color='tuda:pink', label='Rollout w/o Control', zorder=3)
        ax.plot(domain_test, latent_trajectory_without_control_test, color='tuda:pink', ls='dashed', label='Rollout w/o Control (Prediction)', zorder=3)

        if PLOT_CONFIDENCE:
            confidence = 2 * np.sqrt(util.normalize_covariances(latent_covariance[:, dim, dim]))
            upper = latent_covariance[:, dim] + confidence
            lower = latent_covariance[:, dim] - confidence
            ax.fill_between(domain, upper, lower, color='tuda:pink', alpha=0.2, label='Confidence w/o Control', zorder=2)
    # Smoothed trajectory and prediction.
    ax.plot(domain_train, latent_trajectory_smoothed[dim, :], color='tuda:orange', ls='dashdot', label='Smoothed', zorder=5)
    ax.plot(domain_test, latent_pred_trajectory[:, dim], color='tuda:orange', ls='dotted', label='Smoothed (Prediction)', zorder=5)
    if PLOT_CONFIDENCE:
        confidence = 2 * np.sqrt(util.normalize_covariances(result.V_hat[n, dim, dim, :]))
        upper_a = latent_trajectory_smoothed[dim, :] + confidence
        lower_a = latent_trajectory_smoothed[dim, :] - confidence
        confidence = 2 * np.sqrt(util.normalize_covariances(latent_pred_covariance[1:, dim, dim]))
        upper_b = latent_pred_trajectory[1:, dim] + confidence
        lower_b = latent_pred_trajectory[1:, dim] - confidence
        upper = np.concatenate([upper_a, upper_b], axis=0)
        lower = np.concatenate([lower_a, lower_b], axis=0)
        ax.fill_between(domain, upper, lower, color='tuda:orange', alpha=0.2, label='Smoothed Confidence', zorder=4)
    # Rollout w/ control inputs.
    if PLOT_ROLLOUT:
        ax.plot(domain_train, latent_trajectory_train, color='tuda:blue', label='Rollout', zorder=7)
        ax.plot(domain_test, latent_trajectory_test, color='tuda:blue', ls='dashed', label='Rollout (Prediction)', zorder=7)
        if PLOT_CONFIDENCE:
            confidence = 2 * np.sqrt(util.normalize_covariances(latent_covariance[:, dim, dim]))
            upper = latent_trajectory[:, dim] + confidence
            lower = latent_trajectory[:, dim] - confidence
            ax.fill_between(domain, upper, lower, color='tuda:blue', alpha=0.2, label='Rollout Confidence', zorder=6)
    # Prediction boundary and learned initial value.
    ax.axvline(domain_train[-1], color='tuda:red', ls='dotted', label='Prediction Boundary', zorder=1)
    ax.scatter(domain[0], result.m0[dim], marker='*', color='tuda:green', label='Learned Initial Value', zorder=10)
    ax.set_ylabel('Dim. %d' % (dim + 1))


def _plot_observations_rollout(out_dir: str, config: ExperimentConfig, result: ExperimentResult, N: int, observation_trajectories: List[np.ndarray],
                               observation_covariances: List[np.ndarray], observation_trajectories_without_control: List[Optional[np.ndarray]],
                               observation_covariances_without_control: List[np.ndarray], observation_pred_rollout: List[np.ndarray],
                               observation_pred_covariances: List[np.ndarray]):
    domain = np.arange(config.T) * config.h
    domain_train = domain[:config.T_train]
    domain_test = domain[config.T_train - 1:]

    learned_initial_observation = result.g_numpy(result.m0)
    if result.y_shift is not None and result.y_scale is not None:
        learned_initial_observation = result.y_shift + learned_initial_observation * result.y_scale

    if result.V_hat is None:
        observation_trajectories_smoothed = result.g_numpy(result.estimations_latents.transpose((0, 2, 1)).reshape(-1, config.latent_dim)) \
            .reshape((N, config.T_train, config.observation_dim))
        observation_covariances_smoothed = [None] * N
    else:
        observation_trajectories_smoothed, observation_covariances_smoothed = zip(
            *[compute_observations(config, result, result.estimations_latents[n].T, result.V_hat[n, :, :, :].transpose((2, 0, 1))) for n in range(N)])

    for dim, dim_name in enumerate(config.observation_dim_names):
        for n, item in enumerate(
                zip(observation_trajectories[:N], observation_covariances[:N], observation_trajectories_without_control[:N], observation_trajectories_smoothed[:N],
                    observation_covariances_smoothed[:N], observation_covariances_without_control[:N], observation_pred_rollout[:N], observation_pred_covariances[:N])):
            observation_trajectory, observation_covariance, observation_trajectory_without_control, observation_trajectory_smoothed, _, _, _, _ = item
            _, _, _, _, observation_covariance_smoothed, observation_covariance_without_control, observation_pred_trajectory, observation_pred_covariance = item
            with SubplotsAndSave(out_dir, f'rollout-observations-N{n}-D{dim}', place_legend_outside=True) as (fig, ax):
                show_debug_info(fig, config, result)

                _plot_observations_rollout_to_ax(ax, config, dim, dim_name, domain, domain_test, domain_train, learned_initial_observation, n, observation_covariance,
                                                 observation_covariance_smoothed, observation_covariance_without_control, observation_pred_covariance, observation_pred_trajectory,
                                                 observation_trajectory, observation_trajectory_smoothed, observation_trajectory_without_control, result)

                if N > 1:
                    ax.set_title('Sequence %d' % (n + 1))
                ax.set_xlabel('$t$')

    for n, item in enumerate(
            zip(observation_trajectories[:N], observation_covariances[:N], observation_trajectories_without_control[:N], observation_trajectories_smoothed[:N],
                observation_covariances_smoothed[:N], observation_covariances_without_control[:N], observation_pred_rollout[:N], observation_pred_covariances[:N])):
        observation_trajectory, observation_covariance, observation_trajectory_without_control, observation_trajectory_smoothed, _, _, _, _ = item
        _, _, _, _, observation_covariance_smoothed, observation_covariance_without_control, observation_pred_trajectory, observation_pred_covariance = item
        with SubplotsAndSave(out_dir, f'rollout-observations-N{n}',
                             nrows=int(np.ceil(config.observation_dim / 2)),
                             ncols=min(config.observation_dim, 2),
                             place_legend_outside=True,
                             sharex='col',
                             squeeze=False) as (fig, axs):
            show_debug_info(fig, config, result)
            for dim, (ax, dim_name) in enumerate(zip(axs.flatten(), config.observation_dim_names)):
                _plot_observations_rollout_to_ax(ax, config, dim, dim_name, domain, domain_test, domain_train, learned_initial_observation, n, observation_covariance,
                                                 observation_covariance_smoothed, observation_covariance_without_control, observation_pred_covariance, observation_pred_trajectory,
                                                 observation_trajectory, observation_trajectory_smoothed, observation_trajectory_without_control, result)

                if N > 1:
                    ax.set_title('Sequence %d' % (n + 1))
                if dim == config.observation_dim - 1 or dim == config.observation_dim - 2:
                    ax.set_xlabel('$t$')


def _plot_observations_rollout_to_ax(ax, config, dim, dim_name, domain, domain_test, domain_train, learned_initial_observation, n, observation_covariance,
                                     observation_covariance_smoothed, observation_covariance_without_control, observation_pred_covariance, observation_pred_trajectory,
                                     observation_trajectory, observation_trajectory_smoothed, observation_trajectory_without_control, result):
    observation_trajectory_train = observation_trajectory[:config.T_train, dim]
    observation_trajectory_test = observation_trajectory[config.T_train - 1:, dim]
    # Rollout w/o control inputs.
    if PLOT_WITHOUT_CONTROL and PLOT_ROLLOUT and observation_trajectory_without_control is not None:
        observation_trajectory_without_control_train = observation_trajectory_without_control[:config.T_train, dim]
        observation_trajectory_without_control_test = observation_trajectory_without_control[config.T_train - 1:, dim]

        ax.scatter(domain, result.observations_without_control[n, :, dim], s=1, color='tuda:gray', label='Truth w/o Control', zorder=0)
        ax.plot(domain_train, observation_trajectory_without_control_train, color='tuda:pink', label='Rollout w/o Control', zorder=3)
        ax.plot(domain_test, observation_trajectory_without_control_test, color='tuda:pink', ls='dashed', label='Rollout w/o Control (Prediction)', zorder=3)

        if PLOT_CONFIDENCE:
            confidence = 2 * np.sqrt(util.normalize_covariances(observation_covariance_without_control[:, dim, dim]))
            upper = observation_trajectory_without_control[:, dim] + confidence
            lower = observation_trajectory_without_control[:, dim] - confidence
            ax.fill_between(domain, upper, lower, color='tuda:pink', alpha=0.2, label='Confidence w/o Control', zorder=2)
    # Ground truth.
    ax.scatter(domain, result.observations[n, :, dim], s=1, color='black', label='Truth', zorder=1)
    # Smoothed trajectory and prediction.
    ax.plot(domain_train, observation_trajectory_smoothed[:, dim], color='tuda:orange', ls='dashdot', label='Smoothed', zorder=5)
    ax.plot(domain_test, observation_pred_trajectory[:, dim], color='tuda:orange', ls='dotted', label='Smoothed (Prediction)', zorder=5)
    if PLOT_CONFIDENCE:
        confidence = 2 * np.sqrt(util.normalize_covariances(observation_covariance_smoothed[:, dim, dim]))
        upper_a = observation_trajectory_smoothed[:, dim] + confidence
        lower_a = observation_trajectory_smoothed[:, dim] - confidence
        confidence = 2 * np.sqrt(util.normalize_covariances(observation_pred_covariance[1:, dim, dim]))
        upper_b = observation_pred_trajectory[1:, dim] + confidence
        lower_b = observation_pred_trajectory[1:, dim] - confidence
        upper = np.concatenate([upper_a, upper_b], axis=0)
        lower = np.concatenate([lower_a, lower_b], axis=0)
        ax.fill_between(domain, upper, lower, color='tuda:orange', alpha=0.2, label='Smoothed Confidence', zorder=4)
    # Rollout w/ control inputs.
    if PLOT_ROLLOUT:
        ax.plot(domain_train, observation_trajectory_train, color='tuda:blue', label='Rollout', zorder=7)
        ax.plot(domain_test, observation_trajectory_test, color='tuda:blue', ls='dashed', label='Rollout (Prediction)', zorder=7)
        if PLOT_CONFIDENCE:
            confidence = 2 * np.sqrt(util.normalize_covariances(observation_covariance[:, dim, dim]))
            upper = observation_trajectory[:, dim] + confidence
            lower = observation_trajectory[:, dim] - confidence
            ax.fill_between(domain, upper, lower, color='tuda:blue', alpha=0.2, label='Rollout Confidence', zorder=6)
    # Prediction boundary and learned initial value.
    ax.axvline(domain_train[-1], color='tuda:red', ls='dotted', label='Prediction Boundary', zorder=1)
    ax.scatter(domain[0], learned_initial_observation[dim], marker='*', color='tuda:green', label='Learned Initial Value', zorder=10)
    ax.set_ylabel(dim_name)


def _plot_lunar_lander(out_dir: str, config: ExperimentConfig, result: ExperimentResult, N: int, observation_trajectories: List[np.ndarray]):
    learned_initial_observation = result.g_numpy(result.m0)
    if result.y_shift is not None and result.y_scale is not None:
        learned_initial_observation = result.y_shift + learned_initial_observation * result.y_scale

    observation_trajectories_smoothed = result.g_numpy(result.estimations_latents.transpose((0, 2, 1)).reshape(-1, config.latent_dim)) \
        .reshape((N, config.T_train, config.observation_dim))

    with SubplotsAndSave(out_dir, 'lunar-lander', 1, N,
                         sharex='col',
                         sharey='row',
                         figsize=figsize(1, N),
                         squeeze=False) as (fig, axs):
        show_debug_info(fig, config, result)
        for n, (ax, observation_trajectory, observation_trajectory_smoothed) in enumerate(zip(axs.flatten(), observation_trajectories[:N], observation_trajectories_smoothed[:N])):
            truth_trajectory_x_train = result.observations[n, :config.T_train, 0]
            truth_trajectory_y_train = result.observations[n, :config.T_train, 1]
            truth_trajectory_x_test = result.observations[n, config.T_train - 1:, 0]
            truth_trajectory_y_test = result.observations[n, config.T_train - 1:, 1]
            observation_trajectory_x_train = observation_trajectory[:config.T_train, 0]
            observation_trajectory_y_train = observation_trajectory[:config.T_train, 1]
            observation_trajectory_x_test = observation_trajectory[config.T_train - 1:, 0]
            observation_trajectory_y_test = observation_trajectory[config.T_train - 1:, 1]
            observation_trajectory_smoothed_x = observation_trajectory_smoothed[:, 0]
            observation_trajectory_smoothed_y = observation_trajectory_smoothed[:, 1]

            # Ground truth.
            ax.scatter(truth_trajectory_x_train, truth_trajectory_y_train, s=1, color='tuda:black', label='Truth')
            ax.scatter(truth_trajectory_x_test, truth_trajectory_y_test, s=1, color='tuda:gray', label='Truth (Test)')

            # Smoothed trajectory.
            ax.scatter(observation_trajectory_smoothed_x, observation_trajectory_smoothed_y, s=1, color='tuda:orange', label='Smoothed')

            # Rollout w/ control inputs.
            ax.scatter(observation_trajectory_x_train, observation_trajectory_y_train, s=1, color='tuda:blue', label='Rollout')
            ax.scatter(observation_trajectory_x_test, observation_trajectory_y_test, s=1, color='tuda:purple', label='Rollout (Prediction)')

            # Prediction boundary and learned initial value.
            ax.scatter(learned_initial_observation[0], learned_initial_observation[1], marker='*', color='tuda:green', label='Learned Initial Value')

            ax.set_title('Sequence %d' % (n + 1))
            ax.set_xlabel(r'$x$')
            ax.set_ylabel(r'$y$')
            ax.legend()
