"""
--- Day 20: Pulse Propagation ---
With your help, the Elves manage to find the right parts and fix all of the machines. Now,
they just need to send the command to boot up the machines and get the sand flowing again.

The machines are far apart and wired together with long cables. The cables don't connect to the
machines directly, but rather to communication modules attached to the machines that perform
various initialization tasks and also act as communication relays.

Modules communicate using pulses. Each pulse is either a high pulse or a low pulse. When a module
sends a pulse, it sends that type of pulse to each module in its list of destination modules.

There are several different types of modules:

Flip-flop modules (prefix %) are either on or off; they are initially off. If a flip-flop module
receives a high pulse, it is ignored and nothing happens. However, if a flip-flop module receives
a low pulse, it flips between on and off. If it was off, it turns on and sends a high pulse. If
it was on, it turns off and sends a low pulse.

Conjunction modules (prefix &) remember the type of the most recent pulse received from each of
their connected input modules; they initially default to remembering a low pulse for each input.
When a pulse is received, the conjunction module first updates its memory for that input. Then,
if it remembers high pulses for all inputs, it sends a low pulse; otherwise, it sends a high pulse.

There is a single broadcast module (named broadcaster). When it receives a pulse, it sends the
same pulse to all of its destination modules.

Here at Desert Machine Headquarters, there is a module with a single button on it called, aptly,
the button module. When you push the button, a single low pulse is sent directly to the
broadcaster module.

After pushing the button, you must wait until all pulses have been delivered and fully handled
before pushing it again. Never push the button if modules are still processing pulses.

Pulses are always processed in the order they are sent. So, if a pulse is sent to modules a, b,
and c, and then module a processes its pulse and sends more pulses, the pulses sent to modules b
and c would have to be handled first.

The module configuration (your puzzle input) lists each module. The name of the module is
preceded by a symbol identifying its type, if any. The name is then followed by an arrow and a
list of its destination modules. For example:

broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
In this module configuration, the broadcaster has three destination modules named a, b,
and c. Each of these modules is a flip-flop module (as indicated by the % prefix). a outputs to b
which outputs to c which outputs to another module named inv. inv is a conjunction module (as
indicated by the & prefix) which, because it has only one input, acts like an inverter (it sends
the opposite of the pulse type it receives); it outputs to a.

By pushing the button once, the following pulses are sent:

button -low-> broadcaster
broadcaster -low-> a
broadcaster -low-> b
broadcaster -low-> c
a -high-> b
b -high-> c
c -high-> inv
inv -low-> a
a -low-> b
b -low-> c
c -low-> inv
inv -high-> a
After this sequence, the flip-flop modules all end up off, so pushing the button again repeats
the same sequence.

Here's a more interesting example:

broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
This module configuration includes the broadcaster, two flip-flops (named a and b),
a single-input conjunction module (inv), a multi-input conjunction module (con), and an untyped
module named output (for testing purposes). The multi-input conjunction module con watches the
two flip-flop modules and, if they're both on, sends a low pulse to the output module.

Here's what happens if you push the button once:

button -low-> broadcaster
broadcaster -low-> a
a -high-> inv
a -high-> con
inv -low-> b
con -high-> output
b -high-> con
con -low-> output
Both flip-flops turn on and a low pulse is sent to output! However, now that both flip-flops are
on and con remembers a high pulse from each of its two inputs, pushing the button a second time
does something different:

button -low-> broadcaster
broadcaster -low-> a
a -low-> inv
a -low-> con
inv -high-> b
con -high-> output
Flip-flop a turns off! Now, con remembers a low pulse from module a, and so it sends only a high
pulse to output.

Push the button a third time:

button -low-> broadcaster
broadcaster -low-> a
a -high-> inv
a -high-> con
inv -low-> b
con -low-> output
b -low-> con
con -high-> output
This time, flip-flop a turns on, then flip-flop b turns off. However, before b can turn off,
the pulse sent to con is handled first, so it briefly remembers all high pulses for its inputs
and sends a low pulse to output. After that, flip-flop b turns off, which causes con to update
its state and send a high pulse to output.

Finally, with a on and b off, push the button a fourth time:

button -low-> broadcaster
broadcaster -low-> a
a -low-> inv
a -low-> con
inv -high-> b
con -high-> output
This completes the cycle: a turns off, causing con to remember only low pulses and restoring all
modules to their original states.

To get the cables warmed up, the Elves have pushed the button 1000 times. How many pulses got
sent as a result (including the pulses sent by the button itself)?

In the first example, the same thing happens every time the button is pushed: 8 low pulses and 4
high pulses are sent. So, after pushing the button 1000 times, 8000 low pulses and 4000 high
pulses are sent. Multiplying these together gives 32000000.

In the second example, after pushing the button 1000 times, 4250 low pulses and 2750 high pulses
are sent. Multiplying these together gives 11687500.

Consult your module configuration; determine the number of low pulses and high pulses that would
be sent after pushing the button 1000 times, waiting for all pulses to be fully handled after
each push of the button. What do you get if you multiply the total number of low pulses sent by
the total number of high pulses sent?

Answer: 1020211150
"""
"""
-- Part Two ---
The final machine responsible for moving the sand down to Island Island has a module attached 
named rx. The machine turns on when a single low pulse is sent to rx.

Reset all modules to their default states. Waiting for all pulses to be fully handled after each 
button press, what is the fewest number of button presses required to deliver a single low pulse 
to the module named rx?

Answer: 238815727638557  
"""

import math

modules = dict()

with open('input/input_20.txt') as f:
    for line in f:
        line = line.rstrip()

        module, destination = line.split(' -> ')
        m_type = None
        if module != 'broadcaster':
            m_type = module[0]
            module = module[1:]

        modules[module] = (m_type, destination.split(', '))


def part1():
    low = 0
    high = 0

    input_map = dict()
    memory = dict()

    for module, (m_type, destination) in modules.items():
        for d in destination:
            input_map[d] = input_map.get(d, []) + [module]

    for module, (m_type, destination) in modules.items():
        if m_type == '%':
            memory[module] = False
        elif m_type == '&':
            memory[module] = {i: False for i in input_map[module]}

    for _ in range(1000):
        queue = [(None, 'broadcaster', False)]

        while queue:
            new_queue = []

            for source, module, is_high in queue:
                if is_high:
                    high += 1
                else:
                    low += 1

                if module not in modules:
                    continue

                m_type, destinations = modules[module]

                if m_type is None:
                    for d in destinations:
                        new_queue.append((module, d, is_high))
                elif m_type == '%':
                    if is_high:
                        continue

                    current_state = memory[module]

                    memory[module] = not current_state

                    for d in destinations:
                        new_queue.append((module, d, not current_state))
                elif m_type == '&':
                    memory[module][source] = is_high

                    send_signal = any(
                        [not signal for signal in memory[module].values() if not signal])

                    for d in destinations:
                        new_queue.append((module, d, send_signal))

            queue = new_queue

    return low * high


def part2():
    input_map = dict()
    memory = dict()

    for module, (m_type, destination) in modules.items():
        for d in destination:
            input_map[d] = input_map.get(d, []) + [module]

    for module, (m_type, destination) in modules.items():
        if m_type == '%':
            memory[module] = False
        elif m_type == '&':
            memory[module] = {i: False for i in input_map[module]}

    module = input_map["rx"][0]
    sources = input_map[module]

    low_counts = dict()
    cycle = 0

    while len(low_counts) < len(sources):
        cycle += 1

        queue = [(None, 'broadcaster', False)]

        while queue:
            new_queue = list()

            for source, module, is_high in queue:
                if module in sources:
                    if not is_high:
                        if module not in low_counts:
                            low_counts[module] = cycle

                info = modules.get(module)

                if info is None:
                    continue

                m_type, destinations = info

                if m_type is None:
                    for d in destinations:
                        new_queue.append((module, d, is_high))
                elif m_type == '%':
                    if is_high:
                        continue

                    current_state = memory[module]

                    memory[module] = not current_state

                    for d in destinations:
                        new_queue.append((module, d, not current_state))
                elif m_type == '&':
                    memory[module][source] = is_high

                    send_signal = any(
                        [not signal for signal in memory[module].values() if not signal])

                    for d in destinations:
                        new_queue.append((module, d, send_signal))

            queue = new_queue

    return math.lcm(*low_counts.values())


print(f"Part 1: {str(part1())}")
print(f"Part 2: {str(part2())}")
