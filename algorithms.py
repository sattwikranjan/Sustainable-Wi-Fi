def backoff_algorithm(cw_current, collisions):
    cw_min = 31
    cw_max = 1023

    if collisions > 2:
        cw_new = cw_current * 2
    else:
        cw_new = max(cw_current // 2, cw_min)

    cw_new = max(cw_min, min(cw_new, cw_max))
    return cw_new

def delay_based_algorithm(cw_current, delay_current, qos_threshold):
    cw_min = 31
    cw_max = 1023

    if delay_current <= qos_threshold:
        cw_new = ((cw_current + 1)* 2 )-1 
    else:
        cw_new = ((cw_current + 1)/ 2 )-1  

    cw_new = max(cw_min, min(cw_new, cw_max))
    return cw_new


def qos_based_algorithm(cw_current, delay_current, qos_threshold, remaining_energy, nodes):
    cw_min = 31
    cw_max = 1023
    alpha_min = 4  
    alpha_max = 16  

    # Calculate extremes within the algorithm
    energies = [node.remaining_energy for node in nodes]
    max_energy = max(energies)
    min_energy = min(energies)

    if remaining_energy == max_energy:
        # Node with maximum remaining energy
        if delay_current <= qos_threshold:
            cw_new = cw_current + alpha_min
        else:
            cw_new = cw_current - alpha_max
    elif remaining_energy == min_energy:
        # Node with minimum remaining energy
        if delay_current <= qos_threshold:
            cw_new = cw_current + alpha_max
        else:
            cw_new = cw_current - alpha_min
    else:
        # Other nodes: no change
        cw_new = cw_current

    # Ensure CW stays within bounds
    cw_new = max(cw_min, min(cw_new, cw_max))
    return cw_new

def rank_based_algorithm(cw_current, delay_current, qos_threshold, remaining_energy, nodes):
    cw_min = 31
    cw_max = 1023
    alpha = 8  # Adjustable parameter for CW adjustment

    # Calculate median remaining energy
    energies = sorted(node.remaining_energy for node in nodes)
    median_energy = energies[len(energies) // 2]

    if remaining_energy > median_energy:
        # Node with higher than median energy
        if delay_current <= qos_threshold:
            cw_new = (cw_current + alpha) - 1
        else:
            cw_new = (cw_current - alpha) - 1
    else:
        # Node with lower than median energy
        if delay_current <= qos_threshold:
            cw_new = (cw_current + alpha) - 1
        else:
            cw_new = (cw_current - alpha) - 1

    # Ensure CW stays within bounds
    cw_new = max(cw_min, min(cw_new, cw_max))
    return cw_new
