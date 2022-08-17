import numpy as np
from numpy.typing import ArrayLike, NDArray

def fwd_kinematics(pose: ArrayLike) -> NDArray:
    """From a given joint pose, calculate the cartesian end effector position as seen from the base frame

    Args:
        pose (ArrayLike): Joint pose

    Returns:
        NDArray: Cartesian end effector position as seen from base frame
    """

    # Calculates the H transformation matrix for D-H parameters
    def T(theta, a, d, alpha):
        return np.array([
            [np.cos(theta), -np.sin(theta)*np.cos(alpha), np.sin(theta)*np.sin(alpha), a*np.cos(theta)],
            [np.sin(theta), np.cos(theta)*np.cos(alpha), - np.cos(alpha)*np.sin(alpha), a*np.sin(theta)],
            [0, np.sin(alpha), np.cos(alpha), d],
            [0, 0, 0, 1]])

    a = np.array([0, -0.425, -0.3922, 0, 0, 0])
    d = np.array([0.1625, 0, 0, 0.1333, 0.0997, 0.0996])
    alpha = np.array([np.pi/2, 0, 0, np.pi/2, -np.pi/2, 0])
    loc_ep_pos = np.array([0, 0, 0, 1])  # position of end effector is at the position of it cs

    # Transformation matrix from end effector frame to base frame
    T_60 = T(pose[0], a[0], d[0], alpha[0])
    for i in range(1,6):
        T_60 = T_60@T(pose[i], a[i], d[i], alpha[i])
    
    return (T_60@loc_ep_pos)[:-1]

if __name__=="__main__":
    print(fwd_kinematics([1.2]*6))
    print(fwd_kinematics([0]*6))
    print(fwd_kinematics([5.270894341,
3.316125579,
1.029744259,
3.473205211,
2.094395102,
1.570796327]
))