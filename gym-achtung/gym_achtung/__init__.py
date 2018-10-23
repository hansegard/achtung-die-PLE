from gym.envs.registration import register

register(
    id='AchtungDieKurve-v1',
    entry_point='gym_achtung.envs:AchtungDieKurve',
    timestep_limit=1000,
    reward_threshold=1.0,
    nondeterministic=True,
)