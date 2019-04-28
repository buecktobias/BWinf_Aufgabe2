from collections import namedtuple

Item = namedtuple('Item', 'triangle weight')


def knapsack(allowed_weight, items):
    k = [
        [0 for x in range(allowed_weight + 1)]
        for x in range(len(items) + 1)
    ]

    for next_idx, (item, weights) in enumerate(zip(items, k), 1):
        for w, current_weight in enumerate(weights[1:], 1):
            if item.weight <= w:
                k[next_idx][w] = max(
                    item.weight + weights[w - item.weight],
                    current_weight
                )
            else:
                k[next_idx][w] = current_weight

    return k[-1][-1], list(fetch_items(k, allowed_weight, items))

# find which items are picked


def fetch_items(k, allowed_weight, items):
    for item, weights_p, weights_n in zip(items[::-1], k[-2::-1], k[::-1]):
        if weights_n[allowed_weight] != weights_p[allowed_weight]:
            yield item
            allowed_weight -= item.weight


if __name__ == '__main__':
    items = [

    ]
    max_value, picked = knapsack(180, items)
    print(items)
    print("Maximum value:", max_value)
    print("Value", "Weight")
    for item in reversed(picked):
        pass
        # print(item.weight)