def sample_SSD(scale=1):
    SSD = np.random.exponential(scale=scale) + MIN_SSD
    while SSD > MAX_SSD:
        SSD = np.random.exponential(scale=scale) + MIN_SSD
    return SSD

def getInput(id_text="s999", sess_text="001"):
    textBox = gui.Dlg(title="Experimenter Input")
    textBox.addField("Subject ID: ", id_text)
    textBox.addField("Session: ", sess_text)
    textBox.show()
    if textBox.OK:
        text1 = textBox.data[0]
        text2 = textBox.data[1]
        return text1, text2
    else:
        return text1, text2
    
def get_prob_dist_inputs(n_trials=20, block1=0.1, block2=0.9):
    while True:
        prob_dist = gui.Dlg(title="Probability Distribution of Conditions")
        prob_dist.addText('Enter total number of trials and % of AI trials in each block.')
        prob_dist.addText('There will be 2 blocks only. (0% AI and 90% AI.)')
        prob_dist.addText('Number of trials should be divisible by 2')
        prob_dist.addField('Number of Trials (Total): ', n_trials)
        prob_dist.addField('Block 1 AI % in proportions: ', block1)
        prob_dist.addField('Block 2 AI % in proportions: ', block2)
        prob_dist.show()

        if not prob_dist.OK:
            print('nothing was entered')
            break

        n_trials = prob_dist.data[0]
        block1 = prob_dist.data[1]
        block2 = prob_dist.data[2]

        if n_trials % 2 == 0:
            break
        else:
            print("Error - Please enter a number of total trials divisible by 2.")
    
    return n_trials, block1, block2

def create_conditions_array(stop_trials, ai_trials):
    conditions = np.array([0] * stop_trials + [1] * ai_trials)
    np.random.shuffle(conditions)
    conditions = conditions.astype('object')
    conditions[conditions == 0] = 'stop'
    conditions[conditions == 1] = 'ai'
    return conditions

def setup_trials():
    n_trials, block1, block2 = get_prob_dist_inputs()
    if n_trials == 0:
        return [], 0

    block = n_trials // 2
    ai_trials_block1 = int(block * block1)
    ai_trials_block2 = int(block * block2)
    stop_trials_block1 = block - ai_trials_block1
    stop_trials_block2 = block - ai_trials_block2

    conditions_block1 = create_conditions_array(stop_trials_block1, ai_trials_block1)
    conditions_block2 = create_conditions_array(stop_trials_block2, ai_trials_block2)

    if random.randint(0, 1) == 0:
        conditions = list(conditions_block1) + list(conditions_block2)
    else:
        conditions = list(conditions_block2) + list(conditions_block1)

    return conditions, block


def setupPractice():
    practice_block = np.array([0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

    np.random.shuffle(practice_block)

    # Replacing values with trial types
    practice_block = practice_block.astype("object")
    practice_block[practice_block == 0] = "stop"
    practice_block[practice_block == 1] = "ai"

    return list(practice_block), len(practice_block)