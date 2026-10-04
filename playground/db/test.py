from pathlib import Path
from icecream import ic

ic("===Start===========")
no: list[int] = [0, 1, 2]
ic(type(Path(__file__).as_posix()))
ic(__file__, type(__file__))
for n in no:
    parent_dir: Path = Path(__file__).resolve().parents[n]
    ic(n, parent_dir, type(parent_dir))
    pds = str(parent_dir.as_posix())
    ic(pds, type(pds))
# เพิ่ม path เข้าไปใน sys.path ถ้ายังไม่มีอยู่
# if str(parent_dir) not in sys.path:
#     ic()
#     sys.path.insert(0, str(parent_dir))

# # ตอนนี้สามารถ import parent_module ได้แล้ว
# import parent_module


# def run_child() -> None:
#     # เรียกใช้ function จาก parent_module
#     parent_module.parent_function()


# if __name__ == "__main__":
#     run_child()
