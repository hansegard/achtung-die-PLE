from gym.envs.registration import register

register(
    id='AchtungDieKurveSmallGrid-v0',
    entry_point='gym_achtung.envs:AchtungDieKurveSmallGrid',
    timestep_limit=1000,
    reward_threshold=1.0,
    nondeterministic=True,
)

register(
    id='AchtungDieKurveBigGrid-v0',
    entry_point='gym_achtung.envs:AchtungDieKurveBigGrid',
    timestep_limit=10000,
    reward_threshold=1.0,
    nondeterministic=True,
)

register(
    id='AchtungDieKurveAgainstPlayer-v0',
    entry_point='gym_achtung.envs:AchtungDieKurveAgainstPlayer',
    timestep_limit=10000,
    reward_threshold=1.0,
    nondeterministic=True,
)
