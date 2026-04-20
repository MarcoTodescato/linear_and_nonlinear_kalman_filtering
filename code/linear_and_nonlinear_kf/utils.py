
import numpy as np


def simulate_linear_model(n_steps: int,
                          dt: float,
                          p0: float,
                          v0: float,
                          a0: float,
                          sigma_j: float,
                          sigma_y_pos: float,
                          sigma_y_acc: float,
                          seed: int = 0):
    """
    Generate simulated motion of a point in 1D according to linear model
    
    Args:
        n_steps (int): number of steps to simulate.
        dt (float): time step.
        p0 (float): initial position.
        v0 (float): initial velocity.
        a0 (float): initial acceleration.
        sigma_j (float): standard deviation/intensity of jerk.
        sigma_y_pos (float): standard deviation of position measurement noise. If set <0, auto set to 0 ==> equal to true values
        sigma_y_acc (float): standard deviation of acceleration measurement noise. If set <0, auto set to 0 ==> equal to true values
        seed (int, optional): random seed for reproducibility. Defaults to 0.

    Returns:
        tuple: (true_pos, true_vel, y_pos, y_acc) arrays of positions, velocities, pos and acc measurements.
    
    Sensors:
        position measurement: y_pos = x + N(0, sigma_y_pos^2)
        acceleration measurement: y_acc = a + N(0, sigma_y_acc^2)
    """
    p = float(p0)
    v = float(v0)
    a = float(a0)

    A = np.array([
        [1.0, dt, 0.5*dt**2],
        [0.0, 1.0, dt],
        [0.0, 0.0, 1.0]
    ])

    H = np.array([
        [1, 0, 0],
        [0, 0, 1]
    ])

    sigma_j = np.max([0, sigma_j]).astype(float)
    sigma_y_pos = np.max([0, sigma_y_pos]).astype(float)
    sigma_y_acc = np.max([0, sigma_y_acc]).astype(float)

    Q = sigma_j**2 * np.array([
        [dt**5/20, dt**4/8,  dt**3/6],
        [dt**4/8,  dt**3/3,  dt**2/2],
        [dt**3/6,  dt**2/2,  dt]
    ])

    R = np.diag([sigma_y_pos**2, sigma_y_acc**2])

    pos, vel, acc = [], [], []
    y_pos, y_acc = [], []
    x = np.array([p, v, a]).reshape(3, 1)

    for k in range(n_steps):
        # acceleration
        rng = np.random.default_rng(seed + k)

        # sample noise
        w = rng.multivariate_normal(np.zeros(3), Q).reshape(3,1)

        # interate/integrate
        x = A @ x + w

        # extract
        p = x[0,0]
        v = x[1,0]
        a = x[2,0]

        # append history
        pos.append(p)
        vel.append(v)
        acc.append(a)

        # noisy pos + acc measurements
        v = rng.multivariate_normal(np.zeros(2), R).reshape(2,1)
        y = H @ x + v
        y_pos.append(y[0, 0])
        y_acc.append(y[1, 0])

    return (np.array(pos), np.array(vel), np.array(acc),
            np.array(y_pos), np.array(y_acc))


def simulate_nonlinear_model(n_steps: int,
                             dt: float,
                             p0: float,
                             v0: float,
                             a0: float,
                             sigma_j: float,
                             sigma_y: float,
                             alpha: float = 0.0,
                             beta: float = 0.0,
                             L: float = 1.0,
                             C: float = 0.,
                             seed: int = 0):
    """
    Simulate a nonlinear 1D motion model with state

        x = [position, velocity, acceleration]^T

    Nonlinear process model:
        p_{k+1} = p_k + dt*v_k + 0.5*dt^2*a_k + w_p
        v_{k+1} = v_k + dt*a_k + w_v
        a_{k+1} = a_k + dt*(-alpha*sin(p_k) - beta*v_k*abs(v_k)) + w_a

    Nonlinear measurement model:
        y_k = sqrt(p_k^2 + L^2) + v_k^m

    where
        w_k ~ N(0, Q)
        v_k^m ~ N(0, sigma_y^2)

    Args:
        n_steps (int): number of simulation steps.
        dt (float): time step.
        p0 (float): initial position.
        v0 (float): initial velocity.
        a0 (float): initial acceleration.
        sigma_j (float): jerk-noise standard deviation/intensity.
        sigma_y (float): measurement noise standard deviation.
        alpha (float, optional): position-dependent nonlinearity coefficient.
        beta (float, optional): nonlinear drag coefficient.
        L (float, optional): offset parameter in the nonlinear measurement model.
        C (float, optional): coefficient for directional info on measurement model.
        seed (int, optional): random seed for reproducibility.

    Returns:
        tuple:
            (
                true_pos,    # shape (n_steps,)
                true_vel,    # shape (n_steps,)
                true_acc,    # shape (n_steps,)
                y_meas       # shape (n_steps,)
            )

    Notes:
        - Setting alpha=0 and beta=0 reduces the process model to the linear
          constant-acceleration model with jerk-driven noise.
        - Measurement y_meas is a nonlinear range-like measurement, not signed position.
    """

    sigma_j = float(max(0.0, sigma_j))
    sigma_y = float(max(0.0, sigma_y))
    L = float(L)

    # Jerk-driven process noise covariance
    Q = sigma_j**2 * np.array([
        [dt**5 / 20.0, dt**4 / 8.0, dt**3 / 6.0],
        [dt**4 / 8.0,  dt**3 / 3.0, dt**2 / 2.0],
        [dt**3 / 6.0,  dt**2 / 2.0, dt]
    ])

    rng = np.random.default_rng(seed)

    x = np.array([[float(p0)],
                  [float(v0)],
                  [float(a0)]])

    pos, vel, acc = [], [], []
    y_meas = []

    for _ in range(n_steps):
        p, v, a = x.flatten()

        # Deterministic nonlinear state update
        x_det = np.array([
            [p + dt * v + 0.5 * dt**2 * a],
            [v + dt * a],
            [a + dt * (-alpha * np.sin(p) - beta * v * abs(v))]
        ])

        # Add process noise
        w = rng.multivariate_normal(mean=np.zeros(3), cov=Q).reshape(3, 1)
        x = x_det + w

        # Extract true state
        p = x[0, 0]
        v = x[1, 0]
        a = x[2, 0]

        pos.append(p)
        vel.append(v)
        acc.append(a)

        # Nonlinear measurement
        y_true = np.sqrt(p**2 + L**2) + C*p
        yk = y_true + rng.normal(0.0, sigma_y)
        y_meas.append(yk)

    return (
        np.array(pos),
        np.array(vel),
        np.array(acc),
        np.array(y_meas)
    )