import gym

from src.envs.angle_pendulum_env import PendulumAngleEnv
from src.envs.modified_acrobot_env import ModifiedAcrobotEnv
from src.envs.uncontrolled_cartpole_env import UncontrolledCartPole

gym.envs.register(id='PendulumAngle-v0', entry_point='src.envs.angle_pendulum_env:PendulumAngleEnv')
gym.envs.register(id='ModifiedAcrobot-v0', entry_point='src.envs.modified_acrobot_env:ModifiedAcrobotEnv')
gym.envs.register(id='UncontrolledCartPole-v0', entry_point='src.envs.uncontrolled_cartpole_env:UncontrolledCartPole')
