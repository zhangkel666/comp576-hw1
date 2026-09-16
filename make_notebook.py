"""Build the COMP 576 HW1 report notebook.

The generated notebook is executed separately with Jupyter so that every code
cell contains authentic IPython output.
"""

from textwrap import dedent

import nbformat as nbf


def md(text: str):
    return nbf.v4.new_markdown_cell(dedent(text).strip())


def code(text: str):
    return nbf.v4.new_code_cell(dedent(text).strip())


nb = nbf.v4.new_notebook()
nb.metadata.update(
    {
        "kernelspec": {
            "display_name": "Python 3 (comp576)",
            "language": "python",
            "name": "python3",
        },
        "language_info": {"name": "python", "version": "3.12.14"},
        "title": "ELEC 576 / COMP 576 — Homework 1",
    }
)

nb.cells = [
    md(
        """
        # ELEC 576 / COMP 576 — Fall 2026
        ## Homework 1 (Assignment 0)

        **Name:** zhangkeli  
        **NetID:** zl210  
        **Date:** September 16, 2026

        This report records the requested environment checks, NumPy linear
        algebra commands, and Matplotlib figures. All Python cells were run in
        Jupyter/IPython using the `comp576` Conda environment.
        """
    ),
    md(
        """
        ## Task 1 — Conda information

        I installed Miniconda and created a separate `comp576` environment.
        I activated it and ran `conda info` in the terminal. The result was:

        ```text
             active environment : comp576
            active env location : /home/zhangke/miniconda3/envs/comp576
                    shell level : 1
               user config file : /home/zhangke/.condarc
         populated config files : /home/zhangke/miniconda3/.condarc
                                  /home/zhangke/miniconda3/condarc.d/anaconda-auth.yml
                  conda version : 25.11.1
            conda-build version : not installed
                 python version : 3.13.11.final.0
                         solver : libmamba (default)
               virtual packages : __archspec=1=zen5
                                  __conda=25.11.1=0
                                  __cuda=12.8=0
                                  __glibc=2.39=0
                                  __linux=6.8.0=0
                                  __unix=0=0
               base environment : /home/zhangke/miniconda3  (writable)
              conda av data dir : /home/zhangke/miniconda3/etc/conda
          conda av metadata url : None
                   channel URLs : https://repo.anaconda.com/pkgs/main/linux-64
                                  https://repo.anaconda.com/pkgs/main/noarch
                                  https://repo.anaconda.com/pkgs/r/linux-64
                                  https://repo.anaconda.com/pkgs/r/noarch
                  package cache : /home/zhangke/miniconda3/pkgs
                                  /home/zhangke/.conda/pkgs
               envs directories : /home/zhangke/miniconda3/envs
                                  /home/zhangke/.conda/envs
                       platform : linux-64
                     user-agent : conda/25.11.1 requests/2.32.5 CPython/3.13.11
                                  Linux/6.8.0-138-generic ubuntu/24.04.4 glibc/2.39
                                  solver/libmamba conda-libmamba-solver/25.11.0
                                  libmambapy/2.3.2 aau/0.7.5 c/. s/. e/.
                        UID:GID : 1010:1010
                     netrc file : None
                   offline mode : False
        ```

        The `python version` line above is the Python used internally by the
        base Conda installation. The activated course environment and this
        notebook use Python 3.12.14, as verified below.
        """
    ),
    code(
        r"""
        import sys
        import numpy as np
        import scipy
        import scipy.linalg
        import matplotlib

        print("Python:", sys.version.split()[0])
        print("NumPy:", np.__version__)
        print("SciPy:", scipy.__version__)
        print("Matplotlib:", matplotlib.__version__)
        """
    ),
    md(
        """
        ## Task 2 — NumPy “Linear algebra equivalents”

        The following cells run every Python command in the current NumPy
        documentation's **Linear algebra equivalents** table. I use a symmetric
        positive-definite 5 × 5 matrix so the same data works for solving,
        Cholesky factorization, eigenvalue calculations, and slicing.
        """
    ),
    code(
        r"""
        import numpy as np
        from scipy import linalg, signal
        from scipy.sparse.linalg import cg, eigs

        np.set_printoptions(precision=4, suppress=True)

        a = np.array([
            [6., 1., 0., 0., 1.],
            [1., 7., 1., 0., 0.],
            [0., 1., 8., 1., 0.],
            [0., 0., 1., 9., 1.],
            [1., 0., 0., 1., 10.],
        ])
        b = np.array([1., 2., 3., 4., 5.])

        print("a =\n", a)
        print("b =", b)
        """
    ),
    md("### Array dimensions and construction"),
    code(
        r"""
        # ndims(a), numel(a), size(a), and size(a,n)
        print("np.ndim(a):", np.ndim(a))
        print("a.ndim:", a.ndim)
        print("np.size(a):", np.size(a))
        print("a.size:", a.size)
        print("np.shape(a):", np.shape(a))
        print("a.shape:", a.shape)
        print("a.shape[1] (MATLAB size(a,2)):", a.shape[1])

        # [1 2 3; 4 5 6]
        literal = np.array([[1., 2., 3.], [4., 5., 6.]])
        print("\n2 x 3 array literal:\n", literal)

        # [A B; C D]
        A = np.array([[1., 2.], [3., 4.]])
        B = np.array([[5.], [6.]])
        C = np.array([[7., 8.]])
        D = np.array([[9.]])
        blocked = np.block([[A, B], [C, D]])
        print("\nnp.block([[A, B], [C, D]]):\n", blocked)
        """
    ),
    md("### Indexing and slicing"),
    code(
        r"""
        # a(end), a(2,5), a(2,:), and a(1:5,:)
        print("a[-1] (last row):", a[-1])
        print("a[1, 4] (row 2, column 5):", a[1, 4])
        print("a[1] (entire second row):", a[1])
        print("a[1, :] (entire second row):", a[1, :])
        print("a[0:5] (first five rows):\n", a[0:5])
        print("a[:5, :] (same slice):\n", a[:5, :])
        """
    ),
    md("### Linear systems"),
    code(
        r"""
        # MATLAB a\\b: solve a x = b
        x_left = linalg.solve(a, b)
        print("linalg.solve(a, b):", x_left)
        print("check a @ x:", a @ x_left)

        # MATLAB b/a: solve x a = b by transposing
        x_right = linalg.solve(a.T, b.T).T
        print("\nright-division equivalent:", x_right)
        print("check x @ a:", x_right @ a)
        """
    ),
    md("### Matrix decompositions and eigenvalue problems"),
    code(
        r"""
        # Singular value decomposition: [U,S,V] = svd(a)
        U, S, Vh = linalg.svd(a)
        V = Vh.T
        print("Singular values S:", S)
        print("SVD reconstruction error:", np.linalg.norm(a - U @ np.diag(S) @ V.T))

        # Cholesky factorization
        L_chol = linalg.cholesky(a, lower=True)
        print("\nCholesky factor L:\n", L_chol)
        print("Cholesky reconstruction error:", np.linalg.norm(a - L_chol @ L_chol.T))

        # Standard eigenvalue problem
        D_eig, V_eig = linalg.eig(a)
        print("\nEigenvalues:", D_eig)
        print("Eigenpair residual:", np.linalg.norm(a @ V_eig - V_eig @ np.diag(D_eig)))

        # Generalized eigenvalue problem a v = lambda B v
        B_general = np.diag([1., 2., 3., 4., 5.])
        D_gen, V_gen = linalg.eig(a, B_general)
        print("\nGeneralized eigenvalues:", D_gen)
        print("Generalized residual:",
              np.linalg.norm(a @ V_gen - B_general @ V_gen @ np.diag(D_gen)))

        # Three eigenvalues/eigenvectors with scipy.sparse.linalg.eigs
        D_sparse, V_sparse = eigs(a, k=3)
        print("\neigs(a, k=3) eigenvalues:", D_sparse)
        print("eigs residual:",
              np.linalg.norm(a @ V_sparse - V_sparse @ np.diag(D_sparse)))
        """
    ),
    code(
        r"""
        # QR decomposition
        Q, R = linalg.qr(a)
        print("QR reconstruction error:", np.linalg.norm(a - Q @ R))
        print("Q orthogonality error:", np.linalg.norm(Q.T @ Q - np.eye(5)))

        # LU decomposition with partial pivoting
        P, L, U_lu = linalg.lu(a)
        print("\nP =\n", P)
        print("L =\n", L)
        print("U =\n", U_lu)
        print("LU reconstruction error:", np.linalg.norm(a - P @ L @ U_lu))

        # Conjugate-gradient solver
        x_cg, info = cg(a, b)
        print("\ncg solution:", x_cg)
        print("cg info (0 means success):", info)
        print("cg residual:", np.linalg.norm(a @ x_cg - b))
        """
    ),
    md("### Fourier transforms, sorting, regression, resampling, and shapes"),
    code(
        r"""
        # Fourier transform and inverse Fourier transform
        fft_result = np.fft.fft(b)
        ifft_result = np.fft.ifft(fft_result)
        print("np.fft.fft(b):", fft_result)
        print("np.fft.ifft(fft_result):", ifft_result)

        # Sort columns and rows
        unsorted = np.array([[3., 1., 9.], [1., 4., 5.], [2., 0., 7.]])
        print("\nOriginal array:\n", unsorted)
        print("np.sort(unsorted, axis=0):\n", np.sort(unsorted, axis=0))
        print("np.sort(unsorted, axis=1):\n", np.sort(unsorted, axis=1))

        # Sort rows by the first column
        I = np.argsort(unsorted[:, 0])
        sorted_rows = unsorted[I, :]
        print("Row order I:", I)
        print("Rows sorted by first column:\n", sorted_rows)
        """
    ),
    code(
        r"""
        # Linear regression Z x = y using least squares
        Z = np.column_stack([np.ones(5), np.arange(5.)])
        y = np.array([1.1, 2.9, 5.2, 6.8, 9.1])
        x_reg, residuals, rank, singular_values = linalg.lstsq(Z, y)
        print("Regression coefficients:", x_reg)
        print("Predictions:", Z @ x_reg)
        print("Rank:", rank)

        # Downsample with Fourier-method resampling
        sample = np.sin(np.linspace(0, 4 * np.pi, 20, endpoint=False))
        q = 2
        downsampled = signal.resample(sample, int(np.ceil(len(sample) / q)))
        print("\nOriginal sample length:", len(sample))
        print("Resampled length:", len(downsampled))
        print("Resampled values:", downsampled)

        # Unique values and squeezing singleton dimensions
        values = np.array([3, 1, 3, 2, 1, 4])
        print("\nnp.unique(values):", np.unique(values))
        singleton = np.arange(6).reshape(1, 6, 1)
        print("Before squeeze:", singleton.shape)
        print("After squeeze:", singleton.squeeze().shape)
        print("Squeezed values:", singleton.squeeze())
        """
    ),
    md(
        """
        ## Task 3 — Required Matplotlib plot

        The following is the assigned script. `savefig` only saves the same
        displayed figure for inclusion in the report.
        """
    ),
    code(
        r"""
        import matplotlib.pyplot as plt

        plt.plot([1, 2, 3, 4], [1, 2, 7, 14])
        plt.axis([0, 6, 0, 20])
        plt.savefig("task3_plot.png", dpi=180, bbox_inches="tight")
        plt.show()
        """
    ),
    md(
        """
        ## Task 4 — Original Matplotlib figure

        I chose a damped cosine signal. Its envelope is
        $\\pm e^{-0.18t}$, and the oscillation is
        $e^{-0.18t}\\cos(2\\pi t)$.
        """
    ),
    code(
        r"""
        t = np.linspace(0, 10, 600)
        envelope = np.exp(-0.18 * t)
        y = envelope * np.cos(2 * np.pi * t)

        fig, ax = plt.subplots(figsize=(9, 4.5))
        ax.plot(t, y, color="#1f77b4", linewidth=2, label="Damped cosine")
        ax.plot(t, envelope, "--", color="#d62728", alpha=0.8, label="Envelope")
        ax.plot(t, -envelope, "--", color="#d62728", alpha=0.8)
        ax.fill_between(t, -envelope, envelope, color="#1f77b4", alpha=0.08)
        ax.axhline(0, color="black", linewidth=0.7)
        ax.set(title="Damped Oscillation", xlabel="Time (s)", ylabel="Amplitude")
        ax.grid(True, alpha=0.25)
        ax.legend()
        fig.tight_layout()
        fig.savefig("task4_plot.png", dpi=180, bbox_inches="tight")
        plt.show()
        """
    ),
    md(
        """
        ## Task 5 — Version-control account

        **GitHub account:** https://github.com/zhangkel666

        ## Task 6 — Public IDE project

        I created this homework as a project, committed it with Git, and pushed
        it to a public GitHub repository.

        **Public repository:** https://github.com/zhangkel666/comp576-hw1

        ## Sources

        1. NumPy Developers, [NumPy for MATLAB users](https://numpy.org/doc/stable/user/numpy-for-matlab-users.html).
        2. Matplotlib Development Team, [Pyplot tutorial](https://matplotlib.org/stable/tutorials/pyplot.html).
        3. Project Jupyter, [Jupyter Documentation](https://docs.jupyter.org/).
        4. Anaconda, [Conda documentation](https://docs.conda.io/).
        """
    ),
]

nbf.write(nb, "COMP576_HW1.ipynb")
print("Created COMP576_HW1.ipynb")

