import os
import shutil
import sys
from argparse import ArgumentParser
from typing import List, Tuple

import numpy as np
import progressbar
from progressbar import Percentage, Bar, ETA

from investigation.observations import compute_observations
from investigation.plot_util import SubplotsAndSave
from investigation.util import load_run, ExperimentMetrics, ExperimentResult, ExperimentConfig, NoResultsFoundException
from src.rollout import compute_rollout

RMSE_METRIC_PREFIX = 'rmse_'
RMSE_NORMALIZED_SUFFIX = '_normalized'

METRIC_LOG_LIKELIHOOD = 'log_likelihood'
METRIC_RMSE_SMOOTHED = f'{RMSE_METRIC_PREFIX}smoothed'
METRIC_RMSE_ROLLOUT = f'{RMSE_METRIC_PREFIX}rollout'
METRIC_RMSE_ROLLOUT_TRAIN = f'{RMSE_METRIC_PREFIX}rollout_train'
METRIC_RMSE_ROLLOUT_PREDICTION = f'{RMSE_METRIC_PREFIX}rollout_prediction'

ACCUMULATION_METHOD_MEAN = 'mean'
ACCUMULATION_METHOD_FIRST = 'first'

RMSE_METRICS = [METRIC_RMSE_SMOOTHED, METRIC_RMSE_ROLLOUT, METRIC_RMSE_ROLLOUT_TRAIN, METRIC_RMSE_ROLLOUT_PREDICTION]
RMSE_METRICS += list([x + RMSE_NORMALIZED_SUFFIX for x in RMSE_METRICS])
ALL_METRICS = [METRIC_LOG_LIKELIHOOD] + RMSE_METRICS
ALL_ACCUMULATION_METHODS = [ACCUMULATION_METHOD_MEAN, ACCUMULATION_METHOD_FIRST]


def calculate_metric(config: ExperimentConfig, result: ExperimentResult, metrics: ExperimentMetrics, n: int, rollout: np.ndarray, smoothed: np.ndarray, metric_name: str) -> float:
    if metric_name == METRIC_LOG_LIKELIHOOD:
        return metrics.log_likelihood[-1]
    if metric_name.startswith(RMSE_METRIC_PREFIX):
        observations = result.observations[n]
        expected = observations
        if metric_name == METRIC_RMSE_SMOOTHED or metric_name == METRIC_RMSE_SMOOTHED + RMSE_NORMALIZED_SUFFIX:
            expected = observations[:config.T_train]
            actual = smoothed
        elif metric_name == METRIC_RMSE_ROLLOUT or metric_name == METRIC_RMSE_ROLLOUT + RMSE_NORMALIZED_SUFFIX:
            actual = rollout
        elif metric_name == METRIC_RMSE_ROLLOUT_TRAIN or metric_name == METRIC_RMSE_ROLLOUT_TRAIN + RMSE_NORMALIZED_SUFFIX:
            expected = observations[:config.T_train]
            actual = rollout[:config.T_train]
        elif metric_name == METRIC_RMSE_ROLLOUT_PREDICTION or metric_name == METRIC_RMSE_ROLLOUT_PREDICTION + RMSE_NORMALIZED_SUFFIX:
            expected = observations[config.T_train:]
            actual = rollout[config.T_train:]
        else:
            assert False
        if metric_name.endswith(RMSE_NORMALIZED_SUFFIX):
            normalization_factor = np.amax(observations, axis=0) - np.amin(observations, axis=0)
            metric = (np.sqrt(((expected - actual) ** 2).mean(axis=0)) / normalization_factor).mean()
        else:
            metric = np.sqrt(((expected - actual) ** 2).mean())
        return metric
    assert False


def calculate_metrics(data: List[Tuple[str, ExperimentConfig, ExperimentResult, ExperimentMetrics, List[np.ndarray], List[np.ndarray]]], metric_names: List[str],
                      accumulation_methods: List[str]) \
        -> List[Tuple[str, str, int, List[Tuple[str, ExperimentConfig, float]]]]:
    res = []
    for metric_name in metric_names:
        for accumulation_method in accumulation_methods:
            print(f'Calculating metric {metric_name} with accumulation method {accumulation_method}.')
            Y = []
            max_N = -1
            for (run_id, config, result, metrics, obs_rollouts, smoothed) in data:
                calculated_metrics = []
                max_N = max(max_N, config.N)
                for n in range(config.N):
                    calculated_metrics.append(calculate_metric(config, result, metrics, n, obs_rollouts[n], smoothed[n], metric_name))
                if accumulation_method == ACCUMULATION_METHOD_MEAN:
                    metric = np.mean(calculated_metrics)
                elif accumulation_method == ACCUMULATION_METHOD_FIRST:
                    metric = calculated_metrics[0]
                else:
                    assert False
                Y.append((run_id, config, metric))
            res.append((metric_name, accumulation_method, max_N, Y))
    return res


def make_title(metric_name: str, accumulation_method: str, max_N: int) -> str:
    if metric_name == METRIC_LOG_LIKELIHOOD:
        label = 'Log-Likelihood'
    elif metric_name.startswith(RMSE_METRIC_PREFIX):
        if metric_name == METRIC_RMSE_SMOOTHED or metric_name == METRIC_RMSE_SMOOTHED + RMSE_NORMALIZED_SUFFIX:
            label = 'RMSE (Smoothed)'
        elif metric_name == METRIC_RMSE_ROLLOUT or metric_name == METRIC_RMSE_ROLLOUT + RMSE_NORMALIZED_SUFFIX:
            label = 'RMSE (Rollout, Complete)'
        elif metric_name == METRIC_RMSE_ROLLOUT_TRAIN or metric_name == METRIC_RMSE_ROLLOUT_TRAIN + RMSE_NORMALIZED_SUFFIX:
            label = 'RMSE (Rollout, Training)'
        elif metric_name == METRIC_RMSE_ROLLOUT_PREDICTION or metric_name == METRIC_RMSE_ROLLOUT_PREDICTION + RMSE_NORMALIZED_SUFFIX:
            label = 'RMSE (Rollout, Prediction)'
        else:
            assert False
        if metric_name.endswith(RMSE_NORMALIZED_SUFFIX):
            label = 'N' + label
    else:
        assert False
    # If there where at most one sequence, we did not need to accumulate anything.
    if max_N > 1:
        if accumulation_method == ACCUMULATION_METHOD_MEAN:
            label += ', Mean over Sequences'
        elif accumulation_method == ACCUMULATION_METHOD_FIRST:
            label += ', First Sequence'
        else:
            assert False
    return label


def make_xlabel(ordinate: str) -> str:
    if ordinate == 'N':
        return 'Number of Training Sequences'
    elif ordinate == 'T_train':
        return 'Training Sequence Length'
    elif ordinate == 'latent_dim':
        return 'Latent Dimensionality'
    assert False


def make_ylabel(metric_name: str) -> str:
    if metric_name == METRIC_LOG_LIKELIHOOD:
        return 'Log-Likelihood'
    if metric_name.startswith(RMSE_METRIC_PREFIX):
        label = 'RMSE'
        if metric_name.endswith(RMSE_NORMALIZED_SUFFIX):
            label = 'N' + label
        return label
    assert False


def main():
    parser = ArgumentParser()
    parser.add_argument('-o', '--out_dir', default='investigation/tmp_figures')
    parser.add_argument('-d', '--result_dir', required=True)
    parser.add_argument('-f', '--from', required=True, type=int, dest='run_from')
    parser.add_argument('-t', '--to', required=True, type=int, dest='run_to')
    parser.add_argument('-m', '--metric', default=','.join(ALL_METRICS))
    parser.add_argument('-a', '--accumulation', default=','.join(ALL_ACCUMULATION_METHODS))
    parser.add_argument('-x', '--ordinate')
    args = parser.parse_args()
    out_dir = args.out_dir
    result_dir = args.result_dir
    run_from = args.run_from
    run_to = args.run_to
    metric_names = args.metric.lower().split(',')
    accumulation_methods = args.accumulation.lower().split(',')
    ordinates = args.ordinate.split(',')

    run_ids = [str(x) for x in range(run_from, run_to + 1)]

    print('Reading results from %s/{%s}.' % (result_dir, ','.join(run_ids)))

    bar = progressbar.ProgressBar(widgets=['        Loading Runs: ', Percentage(), ' ', Bar(), ' ', ETA()], maxval=len(run_ids)).start()
    runs = []
    for i, run_id in enumerate(run_ids):
        try:
            runs.append((run_id, *load_run(f'{result_dir}/{run_id}', 'run', 'metrics')))
        except FileNotFoundError:
            print(f'No run found for id {run_id}! Ignoring.', file=sys.stderr)
        except NoResultsFoundException:
            print(f'No results found for run {run_id}! Ignoring.', file=sys.stderr)
        bar.update(i + 1)
    bar.finish()

    if os.path.isdir(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)

    bar = progressbar.ProgressBar(widgets=['Calculating Rollouts: ', Percentage(), ' ', Bar(), ' ', ETA()], maxval=len(runs)).start()
    data = []
    for i, (run_id, config, result, metrics) in enumerate(runs):
        _, (obs_rollouts, _), _ = compute_rollout(config, result, config.N)
        obs_smoothed, _ = zip(*[compute_observations(config, result, result.estimations_latents[n].T, result.V_hat[n, :, :, :].transpose((2, 0, 1))) for n in range(config.N)])
        data.append((run_id, config, result, metrics, obs_rollouts, obs_smoothed))
        bar.update(i + 1)
    bar.finish()

    print('Calculating metrics.')
    metrics = calculate_metrics(data, metric_names, accumulation_methods)

    print('Saving metrics to CSV.')
    with open(f'{out_dir}/metrics.csv', 'w+') as fh:
        fh.write('run_id,%s,metric_name,accumulation_method,value\n' % ','.join(ordinates))
        for metric_name, accumulation_method, _, Y in metrics:
            for run_id, config, y in Y:
                X = ','.join([str(config.config_dict[ordinate]) for ordinate in ordinates])
                fh.write('%s,%s,%s,%s,%f\n' % (str(run_id), X, metric_name, accumulation_method, y))

    print('Plotting metrics.')
    for ordinate in ordinates:
        X = [run[1].config_dict[ordinate] for run in runs]
        x_data = list(sorted(set(X)))
        for metric_name, accumulation_method, max_N, Y in metrics:
            y_data = []
            for x in x_data:
                y_dat = []
                for _, config, y in Y:
                    if config.config_dict[ordinate] == x:
                        y_dat.append(y)
                y_data.append(y_dat)
            x = np.asarray(x_data)
            y_mean = np.asarray([np.mean(part) for part in y_data])
            y_std = np.asarray([np.std(part) for part in y_data])
            with SubplotsAndSave(out_dir, f'comparison-{metric_name}-{accumulation_method}-vs-{ordinate}') as (fig, ax):
                ax.plot(x, y_mean, color='tuda:blue', label='Average', zorder=1)
                ax.fill_between(x, y_mean - 2 * y_std, y_mean + 2 * y_std, color='tuda:blue', alpha=0.2, label='Standard Deviation (2x)', zorder=1)
                ax.scatter(X, [y for _, _, y in Y], s=1, color='black', label='Data Points', zorder=2)
                ax.set_title(make_title(metric_name, accumulation_method, max_N))
                ax.set_xlabel(make_xlabel(ordinate))
                ax.set_ylabel(make_ylabel(metric_name))
                ax.legend(loc=('lower right' if metric_name == METRIC_LOG_LIKELIHOOD else 'upper right'))


if __name__ == '__main__':
    main()
