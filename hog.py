"""The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact
import random


GOAL_SCORE = 100 # The goal of Hog is to score 100 points.

######################
# Phase 1: Simulator #
######################

# Taking turns

def roll_dice(num_rolls, dice=six_sided):
    """Roll DICE for NUM_ROLLS times.  Returns either the sum of the outcomes,
    or 1 if a 1 is rolled (Pig out). This calls DICE exactly NUM_ROLLS times.

    num_rolls:  The number of dice rolls that will be made; at least 1.
    dice:       A zero-argument function that returns an integer outcome.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    
    roll_sum = 0 #total score for each turn
   
    while num_rolls > 0:
        
        roll = dice()
        if roll == 1:  
            #print("You rolled ",roll )
            #print ("You Pigged Out! You get 1 point this turn")
            return roll # returns 1 as a total score coz "Pig out" rule
        else: 
            #print ("You rolled %d" % (roll))
            roll_sum = roll_sum + roll
            num_rolls = num_rolls - 1 
    #print("Your Total score this turn is, ",roll_sum)
    return roll_sum # returns total score for the turn





def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulates a turn rolling NUM_ROLLS dice, which may be 0 (Free bacon).
    
    If a player chooses to roll zero dice, he scores one more than the largest digit in his opponent's score. 
    For example, if Player 1 has 42 points, Player 0 gains 1 + max(4, 2) = 5 points by rolling zero dice. 
    If Player 1 has 48 points, Player 0 gains 1 + max(4, 8) = 9 points.
    
    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    
    #opponent_score = random.randint(0,100)
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'

    def free_bacon():
        # first if: makes sure, that is score is still one digit long it returns that score.
        str_opponent_score = str(opponent_score)
        if len(str_opponent_score) == 1:
            return opponent_score
        elif len(str_opponent_score) != 1:
            # second if: returns the higher digit of the current score of opponent player
            if int(str_opponent_score[0]) > int(str_opponent_score[1]):
                return int(str_opponent_score[0])
            else:
                return int(str_opponent_score[1])


    #take_turn code
    if num_rolls == 0:
        return free_bacon() + 1 # 
    else:
        return roll_dice(num_rolls) # 


def select_dice(score, opponent_score):
    """
    #Args = Score and Opponent score(player0,player1)
    #Return , Either True if total score of both player is a multiple of 7,
    #or False if its not. This function is used in the "play" function.
    """
    
    if score != 0 and opponent_score != 0:

        if (score + opponent_score) % 7 == 0:
            return True       # Returnuje True
        elif (score + opponent_score) % 7 != 0:
            return False
        else:
            print("Select dice error")

def other(who):
    """Return the other player, for a player WHO numbered 0 or 1.
    This function is not used in the current code.
    >>> other(0)
    1
    >>> other(1)
    0
    """
    
    return 1 - who

def play(strategy0, strategy1, goal=GOAL_SCORE):
    """ Play fuction returns the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first.
    strategy1:  The strategy function for Player 1, who plays second.
    select_dice: Is a function that implements the Hog Wild rule.
    """

    SWINE_MSG = "SWINE SWAP, your score was the exact double so the scores swaped. "
    HOG_WILD_MSG = "Hog Wild, the sum of both players scores were a multiple of 7, so you rolled with 4-sided dice this turn.:( "

    p_0_score = 0
    p_1_score = 0

    def swap():
        nonlocal p_0_score
        nonlocal p_1_score
        if (p_0_score == p_1_score * 2) or \
           (p_1_score == p_0_score * 2):
            print('swap')
            print(p_0_score, p_1_score)
            tmp = p_0_score
            p_0_score = p_1_score
            p_1_score = tmp
            print(p_0_score, p_1_score)
            print('end swap')


    # WHILE ONE PLAYER DOESNT HAVE SCORE 100 , GAME CONTINUES
    print(p_0_score, p_1_score)
    while p_0_score < GOAL_SCORE and p_1_score < GOAL_SCORE:

        if select_dice(p_0_score,p_1_score) == True:
            p_0_score = p_0_score + take_turn(strategy0(p_0_score,p_1_score),p_1_score,dice=four_sided)
        else:
            p_0_score = p_0_score + take_turn(strategy0(p_0_score,p_1_score),p_1_score)
        swap()
        print(p_0_score, p_1_score)

        if select_dice(p_1_score,p_0_score) == True:
            p_1_score = p_1_score + take_turn(strategy1(p_1_score,p_0_score),p_0_score,dice=four_sided)
        else:
            p_1_score = p_1_score + take_turn(strategy1(p_1_score,p_0_score),p_0_score)
        swap()
        print(p_0_score, p_1_score)

    return p_0_score, p_1_score


#######################

# Phase 2: Strategies #
#######################

# Basic Strategy

BASELINE_NUM_ROLLS = 5
BACON_MARGIN = 8

def always_roll(n):
    """Returns a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy

# Experiments

def make_averaged(fn, num_samples=10000):
    """Returns a function that returns the average_value of FN when called.
    
    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    >>> make_averaged(roll_dice, 1000)(2, dice)
    6.0

    In this last example, two different turn scenarios are averaged.
    - In the first, the player rolls a 3 then a 1, receiving a score of 1.
    - In the other, the player rolls a 5 and 6, scoring 11.
    Thus, the average value is 6.0.
    """
 
    def avg(*args):
        
        sum = 0
        for i in range(0, num_samples):
            sum += fn(*args)
      
        return sum/num_samples

    return avg

def max_scoring_num_rolls(dice=six_sided):
    """Returns the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE.  Print all averages as in
    the doctest below.  Assume that dice always returns positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    1 dice scores 3.0 on average
    2 dice scores 6.0 on average
    3 dice scores 9.0 on average
    4 dice scores 12.0 on average
    5 dice scores 15.0 on average
    6 dice scores 18.0 on average
    7 dice scores 21.0 on average
    8 dice scores 24.0 on average
    9 dice scores 27.0 on average
    10 dice scores 30.0 on average
    10
    """
    dice_1 = make_averaged(roll_dice)(1)
    dice_2 = make_averaged(roll_dice)(2)
    dice_3 = make_averaged(roll_dice)(3)
    dice_4 = make_averaged(roll_dice)(4)
    dice_5 = make_averaged(roll_dice)(5)
    dice_6 = make_averaged(roll_dice)(6)
    dice_7 = make_averaged(roll_dice)(7)
    dice_8 = make_averaged(roll_dice)(8)
    dice_9 = make_averaged(roll_dice)(9)
    dice_10 = make_averaged(roll_dice)(10)


    dict_of_avg_rolls = {dice_1:1,dice_2:2, dice_3:3, dice_4:4, dice_5:5, dice_6:6, dice_7:7, dice_8:8, dice_9:9, dice_10:10}
    highest_avg = dict_of_avg_rolls[max(dict_of_avg_rolls)]


    return highest_avg

def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(BASELINE_NUM_ROLLS)):
    """Return the average win rate (0 to 1) of STRATEGY against BASELINE."""
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)
    return (win_rate_as_player_0 + win_rate_as_player_1) / 2 # Average results


def run_experiments():
    """Run a series of strategy experiments and report results."""
    if True: # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if False: # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False: # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False: # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    if False: # Change to True to test final_strategy
        print('final_strategy win rate:', average_win_rate(final_strategy))

    "*** You may add additional experiments as you wish ***"

# Strategies

def bacon_strategy(score, opponent_score):
    """This strategy rolls 0 dice if that gives at least BACON_MARGIN points,
    and rolls BASELINE_NUM_ROLLS otherwise.

    >>> bacon_strategy(0, 0)
    5
    >>> bacon_strategy(70, 50)
    5
    >>> bacon_strategy(50, 70)
    0
    """
    
    def free_bacon(opponent_score):
        # Ak je num_rolls viac ako 0 take_turn mi returnne classic output score
        # ak je num_rolls 0 , take_turn mi returne vacsi digit z opponent score + 1
        
        # first if makes sure, that is score is still one digit long it returns that score.
        str_opponent_score = str(opponent_score)
        if len(str_opponent_score) == 1:
            return opponent_score
        elif len(str_opponent_score) != 1:
            # second is returns the higher digit of the current score of opponent player
            if int(str_opponent_score[0]) > int(str_opponent_score[1]):
                return int(str_opponent_score[0])
            else:
                return int(str_opponent_score[1])  

    if free_bacon(opponent_score) + 1 >= BACON_MARGIN:
        return 0
    else:
        return BASELINE_NUM_ROLLS

    
def swap_strategy(score, opponent_score):
    """This strategy rolls 0 dice when it would result in a beneficial swap and
    rolls BASELINE_NUM_ROLLS if it would result in a harmful swap. It also rolls
    0 dice if that gives at least BACON_MARGIN points and rolls
    BASELINE_NUM_ROLLS otherwise.

    >>> swap_strategy(23, 60) # 23 + (1 + max(6, 0)) = 30: Beneficial swap
    0
    >>> swap_strategy(27, 18) # 27 + (1 + max(1, 8)) = 36: Harmful swap
    5
    >>> swap_strategy(50, 80) # (1 + max(8, 0)) = 9: Lots of free bacon
    0
    >>> swap_strategy(12, 12) # Baseline
    5
    """
    
    def free_bacon(opponent_score):
        # Ak je num_rolls viac ako 0 take_turn mi returnne classic output score
        # ak je num_rolls 0 , take_turn mi returne vacsi digit z opponent score + 1
        
        # first if makes sure, that is score is still one digit long it returns that score.
        str_opponent_score = str(opponent_score)
        if len(str_opponent_score) == 1:
            return opponent_score
        elif len(str_opponent_score) != 1:
            # second is returns the higher digit of the current score of opponent player
            if int(str_opponent_score[0]) > int(str_opponent_score[1]):
                return int(str_opponent_score[0]) + 1
            else:
                return int(str_opponent_score[1]) + 1

        #--------------------------------------------------------
    
    if score > opponent_score:
        return BASELINE_NUM_ROLLS
    elif score < opponent_score and free_bacon(opponent_score) >= 9: 
        return 0

    elif score < opponent_score:
        if 2 * (score + free_bacon(opponent_score))  ==  opponent_score:
            return 0
        else:
            return BASELINE_NUM_ROLLS
    else:
        return BASELINE_NUM_ROLLS


def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    Final strategy , feel free to make change to this code.
    Not yet implemented well enough
      """
    advantage = 30

    def free_bacon(opponent_score):
        # Ak je num_rolls viac ako 0 take_turn mi returnne classic output score
        # ak je num_rolls 0 , take_turn mi returne vacsi digit z opponent score + 1
        
        # first if makes sure, that is score is still one digit long it returns that score.
        str_opponent_score = str(opponent_score)
        if len(str_opponent_score) == 1:
            return opponent_score
        elif len(str_opponent_score) != 1:
            # second is returns the higher digit of the current score of opponent player
            if int(str_opponent_score[0]) > int(str_opponent_score[1]):
                return int(str_opponent_score[0]) + 1
            else:
                return int(str_opponent_score[1]) + 1
        #----------------------------------------------------------------------

    if free_bacon(opponent_score)  >= 9 and (score + free_bacon(opponent_score)) != opponent_score * 2:
        print("bacon")
        return 0
    
    if (score + free_bacon(opponent_score)) * 2 == opponent_score and score >= 6:
        print("imba swap")
        return 0

    if score - advantage > opponent_score:
        print("lead")
        return 3

    return 6


##########################
# Command Line Interface #
##########################

# Note: Functions in this section do not need to be changed.  They use features
#       of Python not yet covered in the course.

def get_int(prompt, min):
    """Return an integer greater than or equal to MIN, given by the user."""
    choice = input(prompt)
    while not choice.isnumeric() or int(choice) < min:
        print('Please enter an integer greater than or equal to', min)
        choice = input(prompt)
    return int(choice)

def interactive_dice():
    """A dice where the outcomes are provided by the user."""
    return get_int('Result of dice roll: ', 1)

def make_interactive_strategy(player):
    """Return a strategy for which the user provides the number of rolls."""
    prompt = 'Number of rolls for Player {0}: '.format(player)
    def interactive_strategy(score, opp_score):
        if player == 1:
            score, opp_score = opp_score, score
        print(score, 'vs.', opp_score)
        choice = get_int(prompt, 0)
        return choice
    return interactive_strategy

def roll_dice_interactive():
    """Interactively call roll_dice."""
    num_rolls = get_int('Number of rolls: ', 1)
    turn_total = roll_dice(num_rolls, interactive_dice)
    print('Turn total:', turn_total)

def take_turn_interactive():
    """Interactively call take_turn."""
    num_rolls = get_int('Number of rolls: ', 0)
    opp_score = get_int('Opponent score: ', 0)
    turn_total = take_turn(num_rolls, opp_score, interactive_dice)
    print('Turn total:', turn_total)

def play_interactive():
    """Interactively call play."""
    strategy0 = make_interactive_strategy(0)
    strategy1 = make_interactive_strategy(1)
    score0, score1 = play(strategy0, strategy1)
    print('Final scores:', score0, 'to', score1)

@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--interactive', '-i', type=str,
                        help='Run interactive tests for the specified question')
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')
    args = parser.parse_args()

    if args.interactive:
        test = args.interactive + '_interactive'
        if test not in globals():
            print('To use the -i option, please choose one of these:')
            print('\troll_dice', '\ttake_turn', '\tplay', sep='\n')
            exit(1)
        try:
            globals()[test]()
        except (KeyboardInterrupt, EOFError):
            print('\nQuitting interactive test')
            exit(0)
    elif args.run_experiments:
        run_experiments()

#debug prints
#print(average_win_rate(final_strategy))
