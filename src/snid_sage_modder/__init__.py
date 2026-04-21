from pathlib import Path
import sys
from importlib import import_module, reload

from snid_sage.interfaces.gui.launcher import main as snid_main

MOD_FOLDER = Path('./snid-sage-mods')
mods: 'list[Mod]' = []


def main() -> int:
    print("Hello from snid-sage-modder!")

    meta_mod = Mod('snid_sage_modder.meta_mod')

    sys.path.append(str(MOD_FOLDER.resolve()))
    for file in MOD_FOLDER.iterdir():
        if (file.is_file() and file.suffix == '.py') or (not file.is_file() and (file/'__init__.py').exists()):
            mods.append(Mod(file.stem))

        


    return snid_main()


def mixin(cls):
    if CURRENT_MOD is None:
        raise RuntimeError('not inside a mod')

    CURRENT_MOD.mixin(cls)

    return cls


def reload_all():
    print('reloading mods...')
    for mod in reversed(mods):
        mod.unload()

    for mod in mods:
        mod.load()


CURRENT_MOD = None


class Mod:
    def __init__(self, name: str) -> None:
        self.name = name
        self.mixins: list[type] = []
        self._loaded = False

        self.load()

    def load(self):
        global CURRENT_MOD
        old = CURRENT_MOD
        CURRENT_MOD = self

        print(f'loading mod {self.name}')

        self.module = import_module(self.name)
        if self._loaded:
            reload(self.module)
        self._loaded = True

        CURRENT_MOD = old
        
    def unload(self):
        for cls in reversed(self.mixins):
            original_base = next(b for b in cls.mro() if not getattr(b, '_is_mixin', False))

            setattr(sys.modules[original_base.__module__], original_base.__name__, cls.mro()[1])

        self.mixins = []
        getattr(self.module, 'unload', lambda: None)()


    def mixin(self, cls: type) -> None:
        self.mixins.append(cls)
        cls._is_mixin = True
        original_base = next(b for b in cls.mro() if not getattr(b, '_is_mixin', False))
        
        mod = sys.modules[original_base.__module__]
        
        old = getattr(mod, original_base.__qualname__, ())

        if not issubclass(cls, old):
            raise RuntimeError(f'Original class of mixin {cls.__name__} not found. ({old=}, {mod=})')
        
        setattr(mod, original_base.__name__, cls)

