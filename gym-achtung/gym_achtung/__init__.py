from gym.envs.registration import register

register(
    id='AchtungDieKurveSmallGrid-v0',
    entry_point='gym_achtung.envs:AchtungDieKurveSmallGrid',
)

register(
    id='AchtungDieKurveBigGrid-v0',
    entry_point='gym_achtung.envs:AchtungDieKurveBigGrid',
)

register(
    id='AchtungDieKurveAgainstPlayer-v0',
    entry_point='gym_achtung.envs:AchtungDieKurveAgainstPlayer',
)

register(
    id='AchtungDieKurveHumanPlayer-v0',
    entry_point='gym_achtung.envs:AchtungDieKurveHumanPlayer',
)
