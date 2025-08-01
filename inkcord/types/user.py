"""Copyright © 2025 sunset-hue

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""

from typing import Callable
from ..resourceid import ResourceID


class User:
    def __init__(self,_data: dict[str,int | str | None]):
        self.__data = _data
        
    
    @property
    def user_id(self) -> ResourceID:
        "The user's id."
        return ResourceID(self.__data["id"]) # pyright: ignore[reportReturnType]
    
    @property
    def username(self) -> str:
        "The user's name."
        return self.__data["username"] # pyright: ignore[reportReturnType]
    
    @property
    def discriminator(self) -> str:
        "User discriminator. Usually 0 for non bot users."
        return self.__data["discriminator"] # pyright: ignore[reportReturnType]
    
    @property
    def global_name(self) -> str:
        "The user's display name."
        return self.__data["global_name"] # pyright: ignore[reportReturnType]
    
    @property
    def avatar(self) -> str:
        return "sss"
    