import sys

from magio.addon import MagioGoAddon

sys.argv = map(lambda arg: arg.decode('utf-8'), sys.argv)
MagioGoAddon().run(sys.argv)
