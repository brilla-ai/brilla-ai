from typing import List


class Taggable:
    tags: List[str] = list

    @classmethod
    def __ignore_fields__(cls):
        return ["tags"]
