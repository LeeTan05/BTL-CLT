import numpy as np

num_bars = int(input("Nhập số thanh: "))
num_nodes = int(input("Nhập số nút: "))

matrix_A = np.zeros((2 * num_nodes, num_bars + num_nodes))
vector_b = np.zeros(2 * num_nodes)

for i in range(num_nodes):
    print(f"\nNhập thông tin cho nút {i + 1}:")

    bars = list(map(int, input(f"Nhập các thanh liên kết với nút {i + 1} (cách nhau bởi dấu cách): ").split()))
    angles = list(map(float, input(f"Nhập góc cách thanh của các nút này (cách nhau bởi dấu cách): ").split()))

    for j, bar in enumerate(bars):
        matrix_A[2 * i][bar - 1] = np.cos(np.radians(angles[j]))
        matrix_A[2 * i + 1][bar - 1] = np.sin(np.radians(angles[j]))

    link_type = input(f"Liên kết tại nút {i + 1} (cố định, di động, hoặc tự do): ").strip().lower()

    if link_type == "cố định":
        matrix_A[2 * i][num_bars + i] = 1
        matrix_A[2 * i + 1][num_bars + i] = 1
    elif link_type == "di động":
        matrix_A[2 * i + 1][num_bars + i] = 1

for i in range(num_nodes):
    force_magnitude = float(input(f"Nhập độ lớn ngoại lực tại nút {i + 1}: "))
    force_angle = float(input(f"Nhập góc của ngoại lực tại nút {i + 1}: "))

    vector_b[2 * i] = -force_magnitude * np.cos(np.radians(force_angle))
    vector_b[2 * i + 1] = -force_magnitude * np.sin(np.radians(force_angle))

try:
    forces = np.linalg.solve(matrix_A, vector_b)
    print("\nỨng lực các thanh và phản lực tại các nút:", forces)
except np.linalg.LinAlgError:
    print("Hệ phương trình không có nghiệm hoặc có vô số nghiệm.")
