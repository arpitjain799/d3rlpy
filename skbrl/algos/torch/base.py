import torch

from skbrl.algos.torch.utility import freeze, unfreeze
from skbrl.algos.torch.utility import to_cuda, to_cpu
from skbrl.algos.torch.utility import torch_api, eval_api


class ImplBase:
    def save_model(self, fname):
        raise NotImplementedError

    def load_model(self, fname):
        raise NotImplementedError

    def predict_value(self, x, action):
        raise NotImplementedError

    @eval_api
    @torch_api
    def predict_best_action(self, x):
        with torch.no_grad():
            return self._predict_best_action(x).cpu().detach().numpy()

    def _predict_best_action(self, x):
        raise NotImplementedError

    @eval_api
    def save_policy(self, fname):
        dummy_x = torch.rand(1, *self.observation_shape, device=self.device)

        # workaround until version 1.6
        freeze(self)

        # dummy function to select best actions
        def _func(x):
            return self._predict_best_action(x)

        traced_script = torch.jit.trace(_func, dummy_x)
        traced_script.save(fname)

        # workaround until version 1.6
        unfreeze(self)

    def to_gpu(self):
        to_cuda(self)
        self.device = 'cuda:0'

    def to_cpu(self):
        to_cpu(self)
        self.device = 'cpu:0'
