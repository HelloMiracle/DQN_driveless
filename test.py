import net
agent = net.dqn()
agent.restore('save/ckpt')
print(agent.egreedy_action([30, 553, 500, 20, 14, 432, 376, 19, 21]))
