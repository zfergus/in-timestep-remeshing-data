import numpy as np
from sympy import *
from sympy.core.numbers import Infinity


def cxx_print(expr, out="result"):
    CSE_results = cse(expr, numbered_symbols("t"), optimizations='basic')
    lines = []
    for helper in CSE_results[0]:
        if isinstance(helper[1], MatrixSymbol):
            lines.append(f'const auto {helper[0]}[{helper[1].size}];')
            lines.append(cxxcode(helper[1], helper[0]))
        else:
            lines.append(
                f'const auto {cxxcode(helper[0])} = {cxxcode(helper[1])};')

    for i, result in enumerate(CSE_results[1]):
        if not isinstance(expr, Matrix):
            lines.append(f'return {cxxcode(result)};')
        else:
            lines.append(cxxcode(result, out))

    return '\n'.join(lines)


def print_function(func, expr, *params, out="result"):
    params = ", ".join(
        [f"double {p}" for param in params for p in np.nditer(
            param, flags=["refs_ok"])]
        + ([f"double {out}[{prod(expr.shape)}]"]
           if isinstance(expr, Matrix) else [])
    )
    return f"""\
{"void" if isinstance(expr, Matrix) else "double"} {func}({params}){{
{cxx_print(expr, out)}
}}""".replace("INFINITY", "std::numeric_limits<double>::infinity()")


def main():
    x_bar = np.array(
        [symbols(f"x{i}_rest y{i}_rest") for i in range(3)]).T
    # u = np.array([symbols(f"u{i}_x u{i}_y") for i in range(3)]).T
    # x = x_bar + u
    x = np.array([symbols(f"x{i} y{i}") for i in range(3)]).T
    Dm = Matrix(x_bar[:, 1:] - x_bar[:, 0].reshape(2, 1))
    Ds = Matrix(x[:, 1:] - x[:, 0].reshape(2, 1))

    F = Ds @ Dm.inv()

    J = F.det()

    # energy = (F.T @ F).trace() / J
    energy = Piecewise(((F.T @ F).trace() / J, J > 0), (Infinity(), J <= 0))

    diff_x = diff(energy, x_bar[0, 0])
    diff_y = diff(energy, x_bar[1, 0])
    jacobian = Matrix([diff_x, diff_y])  # Jacobian
    hessian = Matrix([diff(jacobian, x_bar[0, 0]).T,
                      diff(jacobian, x_bar[1, 0]).T])  # Hessian

    with open("AMIPS2D.cpp", "w") as f:
        f.write("namespace autogen\n{\n")
        f.write(print_function("AMIPS2D_energy", energy, x_bar, x))
        f.write("\n\n")
        f.write(print_function("AMIPS2D_gradient", jacobian, x_bar, x, out="g"))
        f.write("\n\n")
        f.write(print_function("AMIPS2D_hessian", hessian, x_bar, x, out="H"))
        f.write("\n}")


if __name__ == "__main__":
    main()
