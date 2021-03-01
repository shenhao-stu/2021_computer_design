# -*- coding: utf-8 -*-
import numpy as np

#---------------------------------------------------
class RateDecay(object):
    '''Basic class for different types of rate decay,
        e.g., teach forcing ratio, gumbel temperature,
        KL annealing.
    '''
    def __init__(self, burn_down_steps, decay_steps, limit_v):

        self.step = 0
        self.rate = 1.0

        self.burn_down_steps = burn_down_steps
        self.decay_steps = decay_steps

        self.limit_v = limit_v


    def decay_funtion(self):
        # to be reconstructed
        return self.rate


    def do_step(self):
        # update rate
        self.step += 1
        if self.step > self.burn_down_steps:
            self.rate = self.decay_funtion()

        return self.rate


    def get_rate(self):
        return self.rate


class ExponentialDecay(RateDecay):
    def __init__(self, burn_down_steps, decay_steps, min_v):
        super(ExponentialDecay, self).__init__(
            burn_down_steps, decay_steps, min_v)

        self.__alpha = np.log(self.limit_v) / (-decay_steps)

    def decay_funtion(self):
        new_rate = max(np.exp(-self.__alpha*self.step), self.limit_v)
        return new_rate