import argparse
import random
import math

def get_tove_refund(tove_s1: int) -> float:
    match tove_s1:
        case 1:
            return 0.0313
        case 2:
            return 0.0337
        case 3:
            return 0.0362
        case 4:
            return 0.0386
        case 5:
            return 0.0410
        case 6:
            return 0.0434
        case 7:
            return 0.0458
        case 8:
            return 0.0482
        case 9:
            return 0.0506
        case 10:
            return 0.0531

def get_tove_refund_chance(tove_s1: int) -> int:
    match tove_s1:
        case 1:
            return 2
        case 2:
            return 2
        case 3:
            return 3
        case 4:
            return 3
        case 5:
            return 3
        case 6:
            return 4
        case 7:
            return 4
        case 8:
            return 4
        case 9:
            return 5
        case 10:
            return 5

def get_tove_stack_ammo(tove_s1: int) -> int:
    match tove_s1:
        case 1:
            return 1
        case 2:
            return 1
        case 3:
            return 1
        case 4:
            return 1
        case 5:
            return 1
        case 6:
            return 2
        case 7:
            return 2
        case 8:
            return 2
        case 9:
            return 2
        case 10:
            return 2

def get_alice_ammo(alice_s2: int) -> float:
    match alice_s2:
        case 1:
            return 0.1057
        case 2:
            return 0.1384
        case 3:
            return 0.1711
        case 4:
            return 0.2038
        case 5:
            return 0.2365
        case 6:
            return 0.2692
        case 7:
            return 0.3019
        case 8:
            return 0.3346
        case 9:
            return 0.3673
        case 10:
            return 0.4000

def get_alice_refund(alice_s2: int) -> float:
    match alice_s2:
        case 1:
            return 0.1057
        case 2:
            return 0.1384
        case 3:
            return 0.1711
        case 4:
            return 0.2038
        case 5:
            return 0.2365
        case 6:
            return 0.2692
        case 7:
            return 0.3019
        case 8:
            return 0.3346
        case 9:
            return 0.3673
        case 10:
            return 0.4000

def sim(mag_size: int, tove_refund: float, tove_proc: int, tove_stack: int, alice_ammo: int, alice_refund: float):
    bastion_refund = 3
    bastion_count = 0

    tove_refund_amount = tove_refund
    tove_reload_time = 0

    skill_refund = round(mag_size*tove_refund_amount)
    skill_proc = tove_proc
    bullets = mag_size
    total_shots = 0
    skill_stacks = 0
    skill_stack_ammo = tove_stack
    skill_duration = 0
    skill_duration_party = 0
    shot_interval = 5 #number of frames between shots

    stack_drop_self = 0
    stack_drop_party = 0

    reload_count = 0

    alice_ammo_buff = alice_ammo #40% of 60
    alice_ammo_buff_duration = 0
    alice_ammo_refund = alice_refund
    alice_buff_interval = 300
    alice_skill1_interval = 270

    fight_time = 0


    while fight_time < 10800:
        fight_time += shot_interval
        alice_buff_interval -= shot_interval
        alice_skill1_interval -= shot_interval

        if alice_ammo_buff_duration > 0:
            alice_ammo_buff_duration -= shot_interval

            if alice_ammo_buff_duration <= 0:
                mag_size -= alice_ammo_buff

        if alice_buff_interval <= 0:
            alice_ammo_buff_duration = 900
            mag_size += alice_ammo_buff
            bullets += round((mag_size+skill_stack_ammo*skill_stacks)*alice_ammo_refund)
            alice_buff_interval = 1200

        if alice_skill1_interval <= 0:
            alice_skill1_interval = 270
            skill_duration = 5*60

            if skill_stacks < 3:
                skill_stacks +=1

        if bullets > 0:
            total_shots += 1
            bullets -= 1
            bastion_count += 1
            tove_reload_time = 0
        else:
            tove_reload_time -= shot_interval

            if tove_reload_time == 0:
                bullets = mag_size+skill_stack_ammo*skill_stacks
            
            if skill_duration > 0:
                skill_duration -= shot_interval

                if skill_duration <= 0:
                    skill_duration = 0
                    skill_stacks = 0
                    stack_drop_self += 1

            if skill_duration_party > 0:
                skill_duration_party -= shot_interval
                
                if skill_duration_party <= 0:
                    skill_duration_party = 0
                    stack_drop_party += 1
            
            continue

        
        proc = random.randint(0,99) < skill_proc

        if (not proc) and (skill_duration > 0):
            skill_duration -= shot_interval

            if skill_duration <= 0:
                skill_duration = 0
                skill_stacks = 0
                stack_drop_self += 1

        if (not proc) and (skill_duration_party > 0):
            skill_duration_party -= shot_interval
            
            if skill_duration_party <= 0:
                skill_duration_party = 0
                stack_drop_party += 1

        if bastion_count == 10:
            bullets += bastion_refund
            bastion_count = 0

        skill_refund = round((mag_size+skill_stack_ammo*skill_stacks)*tove_refund_amount)
        
        if proc:
            bullets += skill_refund
            skill_duration = 5*60
            skill_duration_party = 5*60

            if skill_stacks < 3:
                skill_stacks += 1

        if bullets > mag_size+skill_stack_ammo*skill_stacks:
            bullets = mag_size+skill_stack_ammo*skill_stacks
        
        if bullets == 0:
                tove_reload_time = 60
                reload_count += 1

    return reload_count, stack_drop_self, stack_drop_party

def running_average(num_runs: int, current_average: float, new_value: float) -> float:
    return (num_runs*current_average+new_value)/(num_runs+1)

def running_var(num_runs: int, current_var: float, new_value: int) -> float:
    return (num_runs*current_var+new_value**2)/(num_runs+1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-ma', '--max_ammo')
    parser.add_argument('-ts1', '--tove_s1')
    parser.add_argument('-as2', '--alice_s2')

    args = parser.parse_args()

    num_sims = 100000

    average = 0
    variance = 0

    num_no_reload = 0
    num_drops_self = 0
    num_drops_party = 0

    tove_refund = get_tove_refund(int(args.tove_s1))
    tove_proc = get_tove_refund_chance(int(args.tove_s1))
    tove_stack = get_tove_stack_ammo(int(args.tove_s1))

    alice_ammo = round(60*get_alice_ammo(int(args.alice_s2)))
    alice_refund = get_alice_refund(int(args.alice_s2))

    print("",end="")

    for i in range(num_sims):
        print("",end='\r')
        #average += sim(int(args.max_ammo), tove_refund, tove_proc, tove_stack, alice_ammo, alice_refund)
        val, drop_self, drop_party = sim(int(args.max_ammo), tove_refund, tove_proc, tove_stack, alice_ammo, alice_refund)

        if val == 0:
            num_no_reload += 1
        
        num_drops_self += drop_self
        
        num_drops_party += drop_party
        
        average = running_average(i, average, val)
        #variance = running_var(i, variance, val)
        print("Average Reloads: {:.1f}".format(average), " Average Drops (self): {:.1f}".format(num_drops_self/(i+1)), " Average Drops (party): {:.1f}".format(num_drops_party/(i+1)), " Progress: {:3.3%}".format((i+1)/num_sims), "   ", end="", sep="")
    
    #standard_dev = math.sqrt(variance - average**2)

    #print ("\n", "Rounds Standard Deviation: {:.0f}\n".format(standard_dev), "Time Standard Deviation: {:.0f}".format(standard_dev/12), end="", sep="")

    print ("\n", "No Reload% : {:3.3%}\n".format(num_no_reload/num_sims), end="", sep="")

if __name__ == '__main__':
    main()
