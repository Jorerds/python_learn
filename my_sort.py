import os, time, datetime


def quick_sort(arr):
    """归并排序
        原理：将数组分成两半，递归排序每一半，然后合并两个已排序的子数组。
        时间复杂度：O(n log n)
        空间复杂度：O(n)
        适用场景：需要稳定排序的场景，处理大数据集。

    Args:
        arr (_type_): 进行排序的数组

    Returns:
        _type_: _description_
    """
    # 归并排序
    if len(arr) <= 1:
        return arr
    # 数组中间的元素（通过数组的总长除与2后向下取整数得到）
    pivot = arr[len(arr) // 2]
    # 分割后小于位于中间元素的数组
    left = [x for x in arr if x < pivot]
    # 中间元素单独作为数组
    middle = [x for x in arr if x == pivot]
    # 分割后大于中间元素的数组
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)


def binary_search(arr, target):
    """二分查找
    原理：在有序数组中，通过不断将搜索区间折半，快速定位目标元素。
    时间复杂度：O(log n)
    空间复杂度：O(1)
    适用场景：有序数据的快速查找。

    Args:
        arr (list): 被搜索的数组
        target (_type_): 搜索的元素
    """
    # 获取数组开始下标
    low = 0
    # 获取数组结束下标
    high = len(arr) - 1
    # while循环，条件不能大于数组最大下标
    while low <= high:
        # 从数组的中间元素开始对元素进行匹配
        mid = (low + high) // 2
        # 匹配到的元素与搜索元素相匹配，则直接返回所在的下标
        if arr[mid] == target:
            return mid
        # 如果当前元素小于搜索元素，则下标往右移动一位
        elif arr[mid] < target:
            low = mid + 1
        # 如果当前元素大于搜索元素，则下标往左移动一位
        else:
            high = mid - 1
    return -1


def fibonacci(n):
    """斐波那契数列

    Args:
        n (int): 数组的长度

    Returns:
        int: 返回数组最后一位元素
    """
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[0], dp[1] = 0, 1
    print(dp)
    for i in range(2, n + 1):
        print(i)
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n], dp


# 回溯算法（全排列）
def permute(nums):
    result = []
    backtrack(nums, [], result)
    return result


def backtrack(nums, path, result):
    if len(path) == len(nums):
        result.append(path.copy())
        return
    for num in nums:
        if num in path:
            continue
        path.append(num)
        backtrack(nums, path, result)
        path.pop()


# 密码破解（全排列测试）
def brute_force_password(chars, target):
    perm_list = permute(chars)
    for perm in perm_list:
        candidate = ''.join(perm)
        if candidate == target:
            return candidate
    return None


def tsp(cities, distances):
    """全排列算法计算行程最优路径和最短距离

    Args:
        cities (list): 城市（地点）集
        distances (dict): 城市（地点）之间的距离字典集

    Returns:
        list,dict: best_path,min_distance
    """
    min_distance = float('inf')
    best_path = None
    # 生成所有可能的排列（从第一个城市开始）
    cities_list = permute(cities[1:])
    for perm in cities_list:
        path = [cities[0]] + list(perm)
        total_distance = 0
        for i in range(len(path) - 1):
            total_distance += distances[path[i]][path[i + 1]]
        if total_distance < min_distance:
            min_distance = total_distance
            best_path = path
    return best_path, min_distance


def tsp_greedy(cities, distances, start_city):
    """贪心算法计算行程最优路径和最短距离

    Args:
        cities (list): 城市（地点）集
        distances (dict): 城市（地点）之间的距离字典集
        start_city (str): 起点城市

    Returns:
        _type_: _description_
    """
    # 初始化
    current_city = start_city
    path = [current_city]
    visited = set([current_city])

    # 总距离初始化0
    total_distance = 0

    # 遍历所有城市
    while len(visited) < len(cities):
        # 找出距离当前城市最近的未访问城市
        min_distance = float('inf')
        next_city = None
        for city in distances[current_city]:
            if city not in visited and distances[current_city][city] < min_distance:
                min_distance = distances[current_city][city]
                next_city = city

        if next_city is not None:
            path.append(next_city)
            visited.add(next_city)
            total_distance += min_distance
            current_city = next_city
        else:
            # 如果没有找到下一个城市，可能无法访问所有城市，返回当前路径
            break

    # 回到起点城市
    if len(visited) == len(cities):
        total_distance += distances[current_city][start_city]
        path.append(start_city)

    return path, total_distance


def heap_sort(arr):
    """堆排序

    Args:
        arr (list): 需要排序数组

    Returns:
        _type_: 排序完成后数组
    """
    n = len(arr)
    # 建堆
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, i, n)
    # 提取元素
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, 0, i)
    return arr


def heapify(arr, i, n):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    if left < n and arr[left] > arr[largest]:
        largest = left
    if right < n and arr[right] > arr[largest]:
        largest = right
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, largest, n)


class UnionFind:
    def __init__(self, size):
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]


if __name__ == '__main__':
    num_list = [30, 1, 80, 60, 48, 78, 64, 100, 1100, 125, 9, 87]
    # a=heap_sort(num_list)
    # print(a)
    # sort_data=quick_sort(num_list)
    # print(sort_data)

    # str_arr=["程序","应用","系统","静态","动态"]
    # sort_arr=sorted(str_arr)
    # num=binary_search(sort_arr,"静态")
    # print(num)

    # n,arr=fibonacci(20)
    # print(n)
    # print(arr)

    cities = ['阳江', '江门', '佛山', '广州']
    distances = {
        '阳江': {'江门': 10, '佛山': 15, '广州': 20},
        '江门': {'阳江': 10, '佛山': 35, '广州': 25},
        '佛山': {'阳江': 15, '江门': 35, '广州': 30},
        '广州': {'阳江': 20, '江门': 25, '佛山': 30}
    }
    # s_time=time.time()
    # best_path, min_distance = tsp(cities, distances)
    # print("最短路径:", best_path)
    # print("最短距离:", min_distance)
    # print(time.time()-s_time)

    # # 选择起点城市
    # start_city='阳江'
    # ss_time=time.time()
    # best_path, min_distance = tsp_greedy(cities, distances, start_city)
    # print("贪心算法找到的路径:", best_path)
    # print("总距离:", min_distance)
    # print(time.time()-ss_time)
    num = 100
    print(num % 10)