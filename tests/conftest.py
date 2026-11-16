"""Lets pytest import Mage block files without installing Mage."""
import importlib.util
import sys
import types

if importlib.util.find_spec("mage_ai") is None:
    decorators = types.ModuleType("mage_ai.data_preparation.decorators")
    for name in ("data_loader", "transformer", "data_exporter", "test"):
        setattr(decorators, name, lambda func: func)
    sys.modules["mage_ai"] = types.ModuleType("mage_ai")
    sys.modules["mage_ai.data_preparation"] = types.ModuleType("mage_ai.data_preparation")
    sys.modules["mage_ai.data_preparation.decorators"] = decorators