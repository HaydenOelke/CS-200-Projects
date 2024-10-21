"""Simple grid model of contagion"""

'''
Charlie Maher CS 211
4.22.24 
PROJECT 3
'''


import mvc # for Listenable
import enum
from typing import List, Tuple
import random
import config



class Health(enum.Enum):
    """Each individual is one discrete state of health"""
    vulnerable = enum.auto()
    asymptomatic = enum.auto()
    symptomatic = enum.auto()
    recovered = enum.auto()
    dead = enum.auto()

    def __str__(self) -> str:
        return self.name

class Population(mvc.Listenable):
    """Simple grid organization of individuals"""
    def __init__(self, rows: int, cols: int):
        super().__init__()
        self.cells = []
        self.nrows = rows
        self.ncols = cols
    # Populate according to the configuration
        for row_i in range(config.get_int("Grid", "Rows")):
            row = []
            for col_i in range(config.get_int("Grid", "Cols")):
                row.append(self._random_individual(row_i, col_i))            
            self.cells.append(row)
              # YOU FILL THIS IN I think i did but ill leave this here to double check 


    def _random_individual(self, row: int, col: int) -> "Individual":
        classes = [(AtRisk, config.get_float("Grid", "Proportion_AtRisk")),
        (Typical, config.get_float("Grid", "Proportion_Typical"))]
        dice = random.random() * 100
        comulative_prob = 0
        for the_class, proportion in classes:
            comulative_prob += proportion
            if dice < comulative_prob:
                return the_class(self, row, col)
            
        return Typical(self,row,col)
                


    def step(self):
        """Next state for all individuals"""
        for row in self.cells:
            for individual in row:
                # Access the state of each individual, not the population
                if individual.state == Health.asymptomatic:
                    if individual._time_in_state > individual.T_Incubate:
                        individual.next_state = Health.symptomatic
                if individual.state == Health.symptomatic:
                    # We could die on any time step before we recover
                    if individual._time_in_state > individual.T_Recover:
                        individual.next_state = Health.recovered
                    elif random.random() < individual.P_Death:
                        individual.next_state = Health.dead

                # Social behavior differs among concrete classes
                individual.social_behavior()
        
        # Social behavior differs among concrete classes
        #self.social_behavior()

    def seed(self):
        """Patient zero"""
        row = random.randint(0,self.nrows-1)
        col = random.randint(0,self.ncols-1)
        self.cells[row][col].infect()
        self.cells[row][col].tick()

    def count_in_state(self, state: Health) -> int:
        """How many individuals are currently in state?"""
        #initilize count then loop through each cell 
        count = 0 
        for row in self.cells:
            for individual in row:
                if individual.state == state :
                    count += 1 
        return count 



    def neighbors(self, num:int, row:int, col:int, dist:int) -> List[Tuple[int, int]]:
        """Give me addresses of up to num neighbors
        up to dist away from here (Manhattan distance).
        """
        result = []
        count = 0
        attempts = 0
        while count < num:
            attempts += 1
            assert attempts < 1000, f"Can't find {num} neighbors at distance {dist}"
            row_step = random.randint(0 - dist, dist)
            col_step = random.randint(0 - dist, dist)
            row_addr = row + row_step
            col_addr = col + col_step
            if row_addr < 0 or row_addr >= self.nrows:
                continue
            if col_addr < 0 or col_addr >= self.ncols:
                continue
            if row_step == 0 and col_step == 0:
                # Skip the central cell
                continue
            neighbor_addr = (row_addr, col_addr)
            result.append(neighbor_addr)
            count += 1
        return result

    
    def visit(self, address: Tuple[int, int]):
        """Who lives there?"""
        row_num, col_num = address
        return self.cells[row_num][col_num]
    

class Individual(mvc.Listenable):
    """An individual in the population, e.g., a person who might
    get and spread disease. The 'state' instance variable is public
    read-only, e.g., listeners can check it.
    """
    def __init__(self, kind: str, region: Population, row: int, col: int):
        # Listener needs its own initialization
        super().__init__()
        self.kind = kind
        self.region = region
        self.row = row
        self.col = col
        # Initially, an Individual is 'vulnerable', not yet infected
        self._time_in_state = 0 # How long in this state?
        self.state = Health.vulnerable
        self.next_state = Health.vulnerable
        # Configuration parameters based on kind
        self.T_Incubate = config.get_int(kind, "T_Incubate")
        self.P_Transmit = config.get_float(kind, "P_Transmit")
        self.T_Recover = config.get_int(kind, "T_Recover")
        self.P_Death = config.get_float(kind, "P_Death")
        self.P_Greet = config.get_float(kind, "P_Greet")
        self.N_Neighbors = config.get_int(kind, "N_Neighbors")
        self.P_Visit = config.get_float(kind, "P_Visit")
        self.Visit_Dist = config.get_int(kind, "Visit_Dist")
        self.neighbors = region.neighbors(num=self.N_Neighbors,
        row=row, col=col,dist=self.Visit_Dist)

    
    def meet(self, other: "Individual"):
        """Two individuals meet. Either may infect
        the other.
        """
        self.maybe_transmit(other) # I might infect you
        other.maybe_transmit(self) # You might infect me

    def maybe_transmit(self, other: "Individual"):
        if not self._is_contagious():
            return
        if not other.state == Health.vulnerable:
            return
        # Transmission is possible. Roll the dice
        if random.random() < self.P_Transmit:
            other.infect()


    def _is_contagious(self) -> bool:
        """SARS COVID 19 apparently spreads before
        the individual is symptomatic.
        """
        return (self.state == Health.symptomatic
        or self.state == Health.asymptomatic)
    

    def tick(self):
        """Time passes"""
        self._time_in_state += 1
        if self.state != self.next_state:
            self.state = self.next_state
            self.notify_all("newstate")
            # Reset clock
            self._time_in_state = 0

            
    def social_behavior(self):
        """A typical individual visits neighbors at random"""
        if random.random() < self.P_Visit:
            addr = random.choice(self.neighbors)
            neighbor = self.region.visit(addr)
        if neighbor.hello(self):
            neighbor.meet(self)


    def hello(self, visitor: "Individual") -> bool:
        """True means 'welcome' and False means 'go away'"""
        raise NotImplementedError("Each class must implement 'hello'")
    
    def infect(self):
        """Called by another individual spreading germs.
        It may also be called on "patient 0" to start simulation.
        """
        if self.state == Health.vulnerable:
            self.next_state = Health.asymptomatic


class Typical(Individual):
    """Typical individual. May visit different neighbors
    each day.
    """
    def __init__(self, region: Population, row: int, col: int):
        # Much of the constructor has been "factored out" into
        # the abstract base class
        super().__init__("Typical", region, row, col)

    def infect(self):
        """Called by another individual spreading germs.
        It may also be called on "patient 0" to start simulation.
        """
        if self.state == Health.vulnerable:
            self.next_state = Health.asymptomatic


    def social_behavior(self):
        """The way a Typical individual interacts with
        Neighbors
        """
        if random.random() < self.P_Visit:
            addr = random.choice(self.neighbors)
            neighbor = self.region.visit(addr)
            if neighbor.hello(self):
                neighbor.meet(self)

    def hello(self, visitor: "Individual") -> bool:
        """True means 'welcome' and False means 'go away'"""
        return True
    

class AtRisk(Individual):
    """Immunocompromised or elderly.
    Vulnerable and cautious.
    """
    def __init__(self, region: "Population", row: int, col: int):
        # Much of the constructor has been "factored out" into
        # the abstract base class
        super().__init__("AtRisk", region, row, col)
        self.prior_visit = None


    def social_behavior(self):
            """The way an AtRisk individual interacts with
            neighbors
            """
            if random.random() >= self.P_Visit:
                # No visits today!
                return
            if self.prior_visit is None:
                # Time for someone new
                addr = random.choice(self.neighbors)
                neighbor = self.region.visit(addr)
                self.prior_visit = neighbor
            else:
                # Second visit to the same person
                neighbor = self.prior_visit
                self.prior_visit = None
            if neighbor.hello(self):
                neighbor.meet(self)

    def hello(self, visitor: "Individual") -> bool:
        """True means 'welcome' and False means 'go away'"""
        return visitor in self.neighbors
    
    def infect(self):
        """Called by another individual spreading germs.
        It may also be called on "patient 0" to start simulation.
        """
        if self.state == Health.vulnerable:
            self.next_state = Health.asymptomatic



class Wanderer(Individual):
    def __init__(self, region , row , col ): 
        super().__init__("Wanderer", row , col , region)

    def social_behavior(self):
       """they have a high probablity of wandering and meeting new people
       """
       if random.random() < self.P_Visit * 2 : # lets double the likelihood of travel
           addr = random.choice(self.neighbors)
           neighbor = self.region.visit(addr)
           if neighbor.hello(self):
               neighbor.meet(self)

    def hello(self, visitor: "Individual") -> bool:
        """ wanderers"""
        return True