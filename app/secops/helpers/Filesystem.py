import pathlib


class Filesystem:
    @staticmethod
    def fileRead(file: str) -> str:
        try:
            with open(file, mode="r") as f:
                return str(f.read())
        except Exception as e:
            raise e



    @staticmethod
    def files(path: str) -> list:
        try:
            def recursiveList(root: pathlib.Path, exclude=("/.git/", )):
                for item in root.iterdir():
                    if any([ex in item.as_posix() for ex in exclude]):
                        continue

                    if item.is_file():
                        yield item.as_posix()
                    if item.is_dir():
                        yield from recursiveList(item)

            return list(recursiveList(pathlib.Path(path)))
        except Exception as e:
            raise e
