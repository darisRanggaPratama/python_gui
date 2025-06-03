def calculate_cube_root():
    try:
        number = float(input("Masukkan angka untuk mencari akar pangkat 3: "))
        if number >= 0:
            result = number ** (1/3)
            print(f"Akar pangkat 3 dari {number} adalah: {result:.4f}")
        else:
            # Handle negative numbers using complex numbers
            result = -(abs(number) ** (1/3))
            print(f"Akar pangkat 3 dari {number} adalah: {result:.4f}")
    except ValueError:
        print("Input tidak valid. Masukkan angka yang benar.")

if __name__ == '__main__':
    calculate_cube_root()