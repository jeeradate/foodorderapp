from pathlib import Path
from icecream import ic

ic("+++++++++++++++++++")

Root_Dir = Path(__file__).parent
ic(Root_Dir, type(Root_Dir))
root_dir = str(Root_Dir.as_posix())
ic(root_dir, type(root_dir))
