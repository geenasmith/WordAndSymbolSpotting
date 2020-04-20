"""
Description: Evaluation script that calculates the precision and recall based on the input dictionaries.
Inputs:      Two dictionaries, one for the algorithm output and a validation set, with keys as the symbol name and values as
             a list of coordinates for the matching symbols.
Returns:     A dictionary with keys as the symbol name and values as a tuple containing the precision and recall metrics for
             the algorithm.
"""
import numpy as np
import random

# VAL_WINDOW: The amount of pixels either left-right or up-down that coordinates can be and still be considered the same
# symbol
VAL_WINDOW = 5

DEBUG = False


def dummy_algorithm():
    output = {}
    for i in range(5):
        output["symbol_" + str(i)] = np.random.randint(low=0, high=50, size=(random.randint(8, 12), 2))
    return output


def evaluate(label_dict, result):
    val_dict = dummy_algorithm()
    test_dict = dummy_algorithm()
    out_dict = {}

    for symbol in val_dict.keys():
        test_set = test_dict[symbol]
        val_set = val_dict[symbol]

        true_pos = 0.0
        for test_coord in test_set:
            for val_coord in val_set:
                if val_coord[0] - VAL_WINDOW < test_coord[0] < val_coord[0] + VAL_WINDOW:
                    if val_coord[1] - VAL_WINDOW < test_coord[1] < val_coord[1] + VAL_WINDOW:
                        true_pos += 1.0
                        break

        false_pos = len(test_set) - true_pos
        total_true = len(val_set) * 1.0

        if DEBUG: print(true_pos, false_pos, total_true)

        precision = true_pos / (true_pos + false_pos)
        recall = true_pos / total_true

        out_dict[symbol] = (precision, recall)

    if DEBUG: print(out_dict)
    for symbol in out_dict.keys():
        print("{} Precision = {:.3} Recall = {:.3}".format(symbol, out_dict[symbol][0], out_dict[symbol][1]))

    return out_dict


def main():
    # For testing purposes
    evaluate(None, None)


if __name__ == "__main__":
    main()
