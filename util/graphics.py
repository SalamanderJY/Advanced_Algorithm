import matplotlib.pyplot as plt
import math


def imshow_with_lines(convex, title):

    centralx = sum(point[0] for point in convex.convex_list) / len(convex.convex_list)
    centraly = sum(point[1] for point in convex.convex_list) / len(convex.convex_list)
    convex.convex_list.sort(key=lambda point: math.atan2(point[0] - centralx, point[1] - centraly))

    tuple_list = []
    # Make the tuple of list of hull
    for i in range(0, len(convex.convex_list)):
        if i == len(convex.convex_list) - 1:
            tuple_list.append([convex.convex_list[i], convex.convex_list[0]])
        else:
            tuple_list.append([convex.convex_list[i], convex.convex_list[i + 1]])

    for i in range(0, len(tuple_list)):
        list_of_x = [tuple_list[i][0][0], tuple_list[i][1][0]]
        list_of_y = [tuple_list[i][0][1], tuple_list[i][1][1]]
        plt.plot(list_of_x, list_of_y, color="red")

    x1 = convex.points.data[:, 0]
    y1 = convex.points.data[:, 1]
    x2 = convex.convex[:, 0]
    y2 = convex.convex[:, 1]
    plt.scatter(x1, y1, color='blue')
    plt.scatter(x2, y2, color='red')
    plt.xlim(convex.num_range[0] - 5, convex.num_range[1] + 5)
    plt.ylim(convex.num_range[0] - 5, convex.num_range[1] + 5)
    plt.axis()
    plt.title(title)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.savefig("../images/" + title + ".png")
    plt.show()


def imshow_performance(x, y, labels, title):
    for i in range(len(y)):
        x1 = x
        y1 = y[i]
        plt.plot(x1, y1, '', label=labels[i])
    plt.title(title)
    plt.legend(loc='upper left')
    plt.xlabel('Data Size')
    plt.ylabel('Running Time')
    plt.savefig("../images/" + title + ".png")
    plt.show()

if __name__ == "__main__":
    imshow_performance([100, 500, 1000, 2000, 3000, 10000],
                       [[0.1348590850830078, 2.7059173583984375, 10.860055446624756, 35.501171350479126,
                         120.68936848640442, 1129.4572291374207],
                        [0.023562192916870117, 0.5626771450042725, 2.2164735794067383, 9.022538423538208,
                         20.19269299507141, 220.06193947792053],
                        [0.015541791915893555, 0.34238338470458984, 1.515127182006836, 5.461269378662109,
                         13.125714540481567, 139.1292941570282]],
                       ["Force Algorithm", "GrahamScan Algorithm", "Quick Convex Hull Algorithm"],
                       "Convex Hull Performance Analysis")

    imshow_performance([100, 200, 500, 1000, 2000, 5000],
                       [[0.0010025501251220703, 0.0034754276275634766, 0.024565696716308594, 0.12875795364379883,
                         0.4296834468841553, 2.177133560180664],
                        [0.2601943016052246, 0.6241929531097412, 3.1645920276641846, 13.585261344909668,
                         57.49008822441101, 514.7037694454193]],
                       ["Greedy Algorithm", "Linear Programming Algorithm"], "Set Covering Performance Analysis")

