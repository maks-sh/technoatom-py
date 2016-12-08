
if __name__ == '__main__':
    def quicksort(list):
        if len(list) == 0:
            return []
        else:
            return quicksort([elem for elem in list if elem < list[0]]) + \
                [list[0]] + \
                quicksort([elem for elem in list if elem > list[0]])

    print(quicksort([1, 2, 5 , 0, -5, 808]))