import matplotlib.pyplot as plt
import numpy as np
from automan.api import Automator, Problem, mdict


class Jacobi(Problem):
    def get_name(self):
        return "jacobi"

    def get_commands(self):
        self.opts = mdict(x=[10, 25, 50, 95], procedure=[
                          "loop", "numpy", "numba"])
        commands = []
        for op in self.opts:
            dir = self.input_path(f'{op["procedure"]}_{op["x"]}', "data.npz")
            base_cmd = f'python jacobi_numba.py -n 100 -o {dir}'
            cmd = f'{base_cmd} --procedure {op["procedure"]} --size {op["x"]}'
            commands.append((f'{op["procedure"]}_{op["x"]}', cmd, None))
        return commands

    def run(self):
        self.make_output_dir()
        x = np.array([10, 25, 50, 95])
        mp = {10: 0, 25: 1, 50: 2, 95: 3}
        y_numpy = np.zeros(x.size, dtype=float)
        y_loop = np.zeros(x.size, dtype=float)
        y_numba = np.zeros(x.size, dtype=float)
        for op in self.opts:
            stdout = self.input_path(
                f'{op["procedure"]}_{op["x"]}', "stdout.txt")
            with open(stdout) as f:
                values = float(f.read().split()[0])
                if op["procedure"] == "numpy":
                    y_numpy[mp[op["x"]]] = values
                elif op["procedure"] == "loop":
                    y_loop[mp[op["x"]]] = values
                elif op["procedure"] == "numba":
                    y_numba[mp[op["x"]]] = values
        # plot results
        plt.plot(x, y_numpy, "o-", label="numpy")
        plt.plot(x, y_loop, "o-", label="loop")
        plt.plot(x, y_numba, "o-", label="numba")
        plt.title("Jacobi")
        plt.grid()
        plt.xlabel("size")
        plt.ylabel("time_taken(s)")
        plt.legend()
        plt.savefig(self.output_path("perf.png"))
        plt.close()
        # save results
        np.savez(
            self.output_path("perf.npz"),
            x=x,
            y_loop=y_loop,
            y_numpy=y_numpy,
            y_numba=y_numba,
        )


class Julia(Problem):
    def get_name(self):
        return "julia"

    def get_commands(self):
        self.opts = mdict(x=[320, 480, 640, 800], procedure=["numpy", "numba"])
        commands = []
        for op in self.opts:
            dir = self.input_path(f'{op["procedure"]}_{op["x"]}', "data.npz")
            base = f'python julia_numba.py -n 100 -o {dir}'
            cmd = f'{base} --procedure {op["procedure"]} --x-pixels {op["x"]}'
            commands.append((f'{op["procedure"]}_{op["x"]}', cmd, None))
        return commands

    def run(self):
        self.make_output_dir()
        x = np.array([320, 480, 640, 800])
        mp = {320: 0, 480: 1, 640: 2, 800: 3}
        y_numpy = np.zeros(x.size, dtype=float)
        y_numba = np.zeros(x.size, dtype=float)
        for op in self.opts:
            stdout = self.input_path(
                f'{op["procedure"]}_{op["x"]}', "stdout.txt")
            with open(stdout) as f:
                values = float(f.read().split()[0])
                if op["procedure"] == "numpy":
                    y_numpy[mp[op["x"]]] = values
                elif op["procedure"] == "numba":
                    y_numba[mp[op["x"]]] = values
        # plot results
        plt.plot(x, y_numpy, "o-", label="numpy", alpha=0.8)
        plt.plot(x, y_numba, "o-", label="numba", alpha=0.9)
        plt.title("Julia")
        plt.grid()
        plt.xlabel("x-pixels")
        plt.ylabel("time_taken(s)")
        plt.legend()
        plt.savefig(self.output_path("perf.png"), format="png")
        plt.close()
        # save results
        np.savez(self.output_path("perf.npz"), x=x,
                 y_numpy=y_numpy, y_numba=y_numba)


if __name__ == "__main__":
    automator = Automator(
        simulation_dir="outputs",
        output_dir="manuscript/figures",
        all_problems=[Jacobi, Julia],
    )
    automator.run()
