from axelrod import Actions, Player, init_args
from axelrod.strategy_transformers import TrackHistoryTransformer

C, D = Actions.C, Actions.D


class TitForTat(Player):
    """
    A player starts by cooperating and then mimics the previous action of the
    opponent.

    Note that the code for this strategy is written in a fairly verbose
    way. This is done so that it can serve as an example strategy for
    those who might be new to Python.

    Names

    - Rapoport's strategy: [Axelrod1980]_
    - TitForTat: [Axelrod1980]_
    """

    # These are various properties for the strategy
    name = 'Tit For Tat'
    classifier = {
        'memory_depth': 1,  # Four-Vector = (1.,0.,1.,0.)
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent):
        """This is the actual strategy"""
        # First move
        if len(self.history) == 0:
            return C
        # React to the opponent's last move
        if opponent.history[-1] == D:
            return D
        return C


class TitFor2Tats(Player):
    """A player starts by cooperating and then defects only after two defects by opponent."""

    name = "Tit For 2 Tats"
    classifier = {
        'memory_depth': 2,  # Long memory, memory-2
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent):
        return D if opponent.history[-2:] == [D, D] else C


class TwoTitsForTat(Player):
    """A player starts by cooperating and replies to each defect by two defections."""

    name = "Two Tits For Tat"
    classifier = {
        'memory_depth': 2,  # Long memory, memory-2
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent):
        return D if D in opponent.history[-2:] else C


class Bully(Player):
    """A player that behaves opposite to Tit For Tat, including first move.

    Starts by defecting and then does the opposite of opponent's previous move.
    This is the complete opposite of TIT FOR TAT, also called BULLY in literature.
    """

    name = "Bully"
    classifier = {
        'memory_depth': 1,   # Four-Vector = (0, 1, 0, 1)
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent):
        return C if opponent.history[-1:] == [D] else D


class SneakyTitForTat(Player):
    """Tries defecting once and repents if punished."""

    name = "Sneaky Tit For Tat"
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent):
        if len(self.history) < 2:
            return "C"
        if D not in opponent.history:
            return D
        if opponent.history[-1] == D and self.history[-2] == D:
            return "C"
        return opponent.history[-1]


class SuspiciousTitForTat(Player):
    """A TFT that initially defects."""

    name = "Suspicious Tit For Tat"
    classifier = {
        'memory_depth': 1, # Four-Vector = (1.,0.,1.,0.)
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent):
        return C if opponent.history[-1:] == [C] else D


class AntiTitForTat(Player):
    """A strategy that plays the opposite of the opponents previous move.
    This is similar to BULLY above, except that the first move is cooperation."""

    name = 'Anti Tit For Tat'
    classifier = {
        'memory_depth': 1,  # Four-Vector = (1.,0.,1.,0.)
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent):
        return D if opponent.history[-1:] == [C] else C


class HardTitForTat(Player):
    """A variant of Tit For Tat that uses a longer history for retaliation."""

    name = 'Hard Tit For Tat'
    classifier = {
        'memory_depth': 3,  # memory-three
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent):
        # Cooperate on the first move
        if not opponent.history:
            return C
        # Defects if D in the opponent's last three moves
        if D in opponent.history[-3:]:
            return D
        # Otherwise cooperates
        return C


class HardTitFor2Tats(Player):
    """A variant of Tit For Two Tats that uses a longer history for
    retaliation."""

    name = "Hard Tit For 2 Tats"
    classifier = {
        'memory_depth': 3,  # memory-three
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent):
        # Cooperate on the first move
        if not opponent.history:
            return C
        # Defects if two consecutive D in the opponent's last three moves
        history_string = "".join(opponent.history[-3:])
        if 'DD' in history_string:
            return D
        # Otherwise cooperates
        return C


class OmegaTFT(Player):
    """OmegaTFT modifies TFT in two ways:
       -- checks for deadlock loops of alternating rounds of (C, D) and (D, C),
       and attempting to break them
       -- uses a more sophisticated retaliation mechanism that is noise tolerant.
    """

    name = "Omega TFT"
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @init_args
    def __init__(self, deadlock_threshold=3, randomness_threshold=8):
        Player.__init__(self)
        self.deadlock_threshold = deadlock_threshold
        self.randomness_threshold = randomness_threshold
        self.randomness_counter = 0
        self.deadlock_counter = 0

    def strategy(self, opponent):
        # Cooperate on the first move
        if len(self.history) == 0:
            return C
        # TFT on round 2
        if len(self.history) == 1:
            return D if opponent.history[-1:] == [D] else C

        # Are we deadlocked? (in a CD -> DC loop)
        if (self.deadlock_counter >= self.deadlock_threshold):
            self.move = C
            if self.deadlock_counter == self.deadlock_threshold:
                self.deadlock_counter = self.deadlock_threshold + 1
            else:
                self.deadlock_counter = 0
        else:
            # Update counters
            if opponent.history[-2:] == [C, C]:
                self.randomness_counter -= 1
            # If the opponent's move changed, increase the counter
            if opponent.history[-2] != opponent.history[-1]:
                self.randomness_counter += 1
            # If the opponent's last move differed from mine, increase the counter
            if self.history[-1] == opponent.history[-1]:
                self.randomness_counter+= 1
            # Compare counts to thresholds
            # If randomness_counter exceeds Y, Defect for the remainder
            if self.randomness_counter >= 8:
                self.move = D
            else:
                # TFT
                self.move = D if opponent.history[-1:] == [D] else C
                # Check for deadlock
                if opponent.history[-2] != opponent.history[-1]:
                    self.deadlock_counter += 1
                else:
                    self.deadlock_counter = 0
        return self.move

    def reset(self):
        Player.reset(self)
        self.randomness_counter = 0
        self.deadlock_counter = 0


class Gradual(Player):
    """
    A player that punishes defections with a growing number of defections
    but after punishing enters a calming state and cooperates no matter what
    the opponent does for two rounds.

    http://perso.uclouvain.be/vincent.blondel/workshops/2003/beaufils.pdf """

    name = "Gradual"
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self):

        Player.__init__(self)
        self.calming = False
        self.punishing = False
        self.punishment_count = 0
        self.punishment_limit = 0

    def strategy(self, opponent):

        if self.calming:
            self.calming = False
            return C

        if self.punishing:
            if self.punishment_count < self.punishment_limit:
                self.punishment_count += 1
                return D
            else:
                self.calming = True
                self.punishing = False
                self.punishment_count = 0
                return C

        if D in opponent.history[-1:]:
            self.punishing = True
            self.punishment_count += 1
            self.punishment_limit += 1
            return D

        return C

    def reset(self):
        Player.reset(self)
        self.calming = False
        self.punishing = False
        self.punishment_count = 0
        self.punishment_limit = 0


@TrackHistoryTransformer(name_prefix=None)
class ContriteTitForTat(Player):
    """
    A player that corresponds to Tit For Tat if there is no noise. In the case
    of a noisy match: if the opponent defects as a result of a noisy defection
    then ContriteTitForTat will become 'contrite' until it successfully
    cooperates..

    Reference: "How to Cope with Noise In the Iterated Prisoner's Dilemma" by
    Wu and Axelrod. Published in Journal of Conflict Resolution, 39 (March
    1995), pp. 183-189.

    http://www-personal.umich.edu/~axe/research/How_to_Cope.pdf
    """

    name = "Contrite Tit For Tat"
    classifier = {
        'memory_depth': 3,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }
    contrite = False

    def strategy(self, opponent):

        if not opponent.history:
            return C

        # If contrite but managed to cooperate: apologise.
        if self.contrite and self.history[-1] == C:
            self.contrite = False
            return C

        # Check if noise provoked opponent
        if self._recorded_history[-1] != self.history[-1]:  # Check if noise
            if self.history[-1] == D and opponent.history[-1] == C:
                self.contrite = True

        return opponent.history[-1]

    def reset(self):
        Player.reset(self)
        self.contrite = False
        self._recorded_history = []


class SlowTitForTwoTats(Player):
    """
    A player plays C twice, then if the opponent plays the same move twice,
    plays that move
    """

    name = 'Slow Tit For Two Tats'
    classifier = {
        'memory_depth': 2,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent):

        # Start with two cooperations
        if len(self.history) < 2:
            return C

        # Mimic if opponent plays the same move twice
        if opponent.history[-2] == opponent.history[-1]:
            return opponent.history[-1]

        # Otherwise cooperate
        return C
        
class AdaptiveTitForTat(Player):
    """Adaptive tit-for-tat model
    If (opponent played C in the last cycle) then
    world = world + rc*(1-world), rc is the adaptation rate for cooperation
    else
    world = world + rd*(0-world), rd is the adaptation rate for defection
    If (world >= 0.5) play C, else play D
    Throughout  an  observation  window,  record  how  many  times  (n)  the  agent’s
    move  has  coincided  with  the  opponent’s  move.  At  regular  intervals  (every
    “window” steps) adapt the rates as follows :
    If (n>threshold) then
    rc = rmin, rd = rmax
    else
    rc = rmax, rd = rmin

    http://users.softlab.ntua.gr/~brensham/Publications/PPSN2000.pdf
    """
    
    name = 'Adaptive Tit for Tat'
    classifier = {
        'memory_depth': 1,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @init_args
    def __init__(self, world=0.5, rate_min=0.1, rate_max=0.8):
    
        super().__init__()
        self.world, self.starting_world = world, world
        self.rate_min, self.starting_rate_min = rate_min, rate_min
        self.rate_max, self.starting_rate_max = rate_max, rate_max
        
    def strategy(self, opponent):
        
        if not self.history:
            return C
        
        if opponent.history[-1] == self.history[-1]:
            rate_c, rate_d = self.rate_min, self.rate_max
        else:
            rate_c, rate_d = self.rate_max, self.rate_min
        
        if opponent.history[-1] == C:
            self.world += rate_c * (1. - self.world)
        else:
            self.world -= rate_d * self.world
        
        if self.world >= 0.5:
            return C
        
        return D
        
    def reset(self):
        
        super().reset()
        self.world = self.starting_world
        self.rate_min = self.starting_rate_min
        self.rate_max = self.starting_rate_max
        self.n = 0
        
    def __repr__(self):
         
        return "%s: world=%s, rate_min=%s, rate_max=%s" % (self.name, 
                                           round(self.world, 2), 
                                           round(self.rate_min, 2),
                                           round(self.rate_max, 2))