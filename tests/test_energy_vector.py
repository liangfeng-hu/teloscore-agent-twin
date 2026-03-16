import unittest

from core.energy_vector import apply_input_signals, default_energy


class TestEnergyVector(unittest.TestCase):
    def test_conflict_signal_raises_u_con(self):
        ev = default_energy("agent_os")
        before = ev.U_con
        apply_input_signals(ev, "这个方案有冲突和失败风险，需要修正。", "agent_os")
        self.assertGreater(ev.U_con, before)

    def test_goal_signal_reduces_u_tel(self):
        ev = default_energy("agent_os")
        before = ev.U_tel
        apply_input_signals(ev, "请给我下一步执行计划和里程碑。", "agent_os")
        self.assertLess(ev.U_tel, before)


if __name__ == "__main__":
    unittest.main()
