import matplotlib.pyplot as plt
def o3():
    print("FOR HIGH  03 LEVELS ")
    print("1. Choose carpooling")
    print("2. Conserve electricity")
    print("3. Prefer walking over running")
    print("4. Avoid outdoor activities when it is hot - either do it  during early day or after sunset")
    print("5. Avoid using an air cleaner that works by generating ozone")


def par():
    print("For high particle levels")
    print("1. Avoid burning of trash or leaves")
    print("2. Stay in a room which has preferably filtered air")
    print("3. Prefer to stay indoors with good filtered air especially people with heart diseases ")
    print("4.Avoid using an air cleaner that works by generating ozone")
    print("5. Check the air quality index daily at https://aqicn.org/city/delhi/")


def solutions():
    choice = input("Solutions for days with: 1. high o3 levels\t2. high particle levels\t3. for both\n")
    if choice == "1":
        o3()

    elif choice == "2":
        par()

    elif choice == "3":
        o3()
        print("---------------------------------------------------------------------------")
        par()


def getMandY(dt):
    if dt == " ":
        return ""
    dt_ = dt.split("/")
    return dt_[1], dt_[2]


def getXLabel(m):
    tick_label = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'June', 7: 'July', 8: 'Aug', 9: 'Sept',
                  10: 'Oct', 11: 'Nov', 12: 'Dec'}
    d_ = []
    for x in m:
        d_.append(tick_label[x])
    return d_


def getYLabel():
    return ['Severe', 'Very Poor', 'Poor', "Moderate", 'Satisfactory', 'Good']


def getAvgFactor(s):
    if s in [4, 6, 9, 11]:
        return 30
    elif s in [1, 3, 5, 7, 8, 10, 12]:
        return 31;
    return 28;


def getAvailableYears(ct, data_):
    if ct not in data_:
        print("Check the city you Entered!")
        return None
    yrs = set()
    for x in data_[ct]:
        yrs.add(x[1])
    return sorted(yrs)


def getAvailableMonths(ct, yr, data_):
    yrs = set()
    for x in data_[ct]:
        if x[1] == yr:
            yrs.add(int(x[0]))
    return sorted(yrs)


def getAQI_Bucket(val):
    if 'Moderate' in val:
        return 3
    elif 'Poor' in val:
        return 2
    elif 'Very Poor' in val:
        return 1
    elif 'Severe' in val:
        return 0
    elif 'Satisfactory' in val:
        return 4
    elif 'Good' in val:
        return 5
    return 0


def getAQI_BucketText(val):
    val -= round(val)
    if val == 3:
        return "Moderate"
    elif val == 2:
        return 'Poor'
    elif val == 1:
        return 'Very Poor'
    elif val == 0:
        return 'Severe'
    elif val == 4:
        return 'Satisfactory'
    elif val == 5:
        return 'Good'
    return 'Very Poor'


def processItem(items, data_, headers):
    m, y = getMandY(items[1])
    items[15] = getAQI_Bucket(items[15])
    key = (m, y)
    lst = {} if (key not in data_) else data_[key]
    j = 0
    for x in headers:
        x = x.rstrip()
        if j > 1:
            k = 0 if (items[j] == "" or items[j] == " ") else items[j]
            l = lst.get(x) if x in lst else 0
            val = float(l) + float(k)
        else:
            val = items[j]
        lst[x] = val
        j += 1
    data_[key] = lst
    return data_


def processItemYearly(datas, ct, years, param):
    x_data = []
    for p in param:
        data_ = {}
        for x in datas[ct]:
            for y in years:
                if x[1] == y:
                    val = data_.get(y) + datas[ct][x][p] if y in data_ else datas[ct][x][p]
                    data_.append(val)
            x_data.append(data_)

    return datas


# def calculateAverageValuesYearly(data):
# for y in data: #city
# months = getAvailableMonths(ct, y, data)
# j = 0
# lst = data[r][s]
# for x in lst: # values
# if j > 1:
# lst[x] = lst.get(x)/av
# j+=1
# return data


def readCSv():
    with open('city_day.csv') as file:
        content = file.readlines()
    header = content[:1][0].split(",")
    header[0] = 'City'
    header[len(header) - 1] = header[len(header) - 1].rstrip()
    rows = content[1:]
    return header, rows


def calculateAverageValues(data_):
    for r in data_:  # city
        for s in data_[r]:  # month,year
            av = getAvgFactor(int(s[0]))
            j = 0
            lst = data_[r][s]
            for x in lst:  # values
                if j > 1:
                    lst[x] = lst.get(x) / av
                j += 1
    return data_


def getDataToDraw(datas, yr, ct, param):
    x_data = []
    for p in param:
        data_ = []
        for x in datas[ct]:
            if x[1] == yr:
                data_.append(datas[ct][x][p])
        x_data.append(data_)

    return x_data


def validateData(d_):
    for x in d_:
        if x not in header[2:len(header)]:
            print("Please check the parameters you entered!")
            return False
        if len(d_) != 1 and x == 'AQI_Bucket':
            print("Please choose  the parameter, AQI_Bucket, independently!")
            return False
    return True


def getTitle(ct, yr, param):
    return ct + "(" + yr + "):" + ','.join(param)


def userInterface(cities, data, header):
    print("Available Cities: ", cities)
    print("Choose a City:")
    ct = input()
    # print("Available Chart Type: ", ["Monthly","Yearly"])
    # ty=input()
    yr = -1
    years = getAvailableYears(ct, data)
    # if(ty=='Monthly'):
    if years is None:
        print("Data is not available in: ", ct)
        return
    print("Available Years: ", years)
    print("Choose a year:")
    yr = input()
    if yr not in years:
        print("Please check the year you entered!")
        return

    print("Available Parameters: ", header[2:len(header)])
    print("Choose the parameters (comma separated for multiple):")
    param = input().split(",")
    if not validateData(param):
        return
    processGraph(data, yr, ct, param)


def processGraph(data_, yr, ct, param):
    dataToDraw = getDataToDraw(data_, yr, ct, param)
    months = getAvailableMonths(ct, yr, data_)
    plotGraph(dataToDraw, getTitle(ct, yr, param), param, months)


def plotGraph(data_, title, param, months):
    tick_label = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
    x = months
    # print(months)
    color = ["green", "blue", "yellow", "red", "black", "purple", "grey", "orange", "brown", "pink", "olive", "cyan",
             "green"]
    for index, d_ in enumerate(data_):
        # plt.scatter(x, d_, label="stars", color=color[index],marker="*", s=30)
        plt.plot(x, d_, color=color[index], label=param[index])
    plt.xticks(x, getXLabel(x))
    plt.xlabel('Months')
    plt.ylabel('Pollution')
    if len(param) == 1 and param[0] == 'AQI_Bucket':
        plt.yticks([0, 1, 2, 3, 4, 5], getYLabel())
    plt.title(title)
    plt.legend()
    plt.show()


def processData(header, rows):
    data = {}
    data_monthly = {}
    for r in rows:
        items = r.split(",")
        city = items[0]
        if city not in data:
            data[city] = {}
        data[city] = processItem(items, data[city], header)
        cities.add(city)
    calculateAverageValues(data)
    # print(data)
    return data


cities = set()
header, rows = readCSv()
data = processData(header, rows)
while True:
    userInterface(cities, data, header)
    if input("DO you want to continue,y/n?") == 'n':
        solutions()
        break