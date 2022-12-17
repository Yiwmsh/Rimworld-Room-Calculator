import PySimpleGUI as sg
import math

# Classes


class Title:
    minValue: float
    title: str

    def __init__(self, minValue: int, title: str):
        self.minValue = minValue
        self.title = title

# Global Variables


roomImpressiveness = 0

spaciousness = 0

scaledWealth = 0
scaledBeauty = 0
scaledSpace = 0
scaledCleanliness = 0

impressivenessTitles = [
    Title(240, 'Wondrously Impressive'),
    Title(170, 'Unbelievably Impressive'),
    Title(120, 'Extremely Impressive'),
    Title(85, 'Very Impressive'),
    Title(65, 'Somewhat Impressive'),
    Title(50, 'Slightly Impressive'),
    Title(40, 'Decent'),
    Title(30, 'Mediocre'),
    Title(20, 'Dull'),
    Title(0, 'Awful')
]

wealthTitles = [
    Title(1000000, 'Unbelievably Luxurious'),
    Title(100000, 'Extremely Luxurious'),
    Title(40000, 'Very Luxurious'),
    Title(10000, 'Luxurious'),
    Title(4000, 'Rich'),
    Title(2000, 'Somewhat Rich'),
    Title(700, 'Mediocre'),
    Title(500, 'Somewhat Poor'),
    Title(0, 'Impoverished')
]

beautyTitles = [
    Title(100, 'Unbelievably Beautiful'),
    Title(50, 'Extremely Beautiful'),
    Title(15, 'Very Beautiful'),
    Title(5, 'Beautiful'),
    Title(2.4, 'Pretty'),
    Title(0, 'Neutral'),
    Title(-3.5, 'Ugly'),
    Title(-1000, 'Hideous')
]

spaceTitles = [
    Title(349.5, 'Extremely Spacious'),
    Title(130, 'Very Spacious'),
    Title(70, 'Quite Spacious'),
    Title(55, 'Somewhat Spacious'),
    Title(29, 'Average-Sized'),
    Title(12.5, 'Rather Tight'),
    Title(0, 'Cramped')
]

cleanlinessTitles = [
    Title(0.4, 'Sterile'),
    Title(-0.05, 'Clean'),
    Title(-0.4, 'Dirty'),
    Title(-1.1, 'Dirty'),
    Title(-1000, 'Very Dirty')
]

# Functions


def updateValueTitles() -> None:
    wealthValue = tryCastFloat(values['-Wealth-'])
    if event == '-Wealth-' and type(wealthValue) == float:
        window['-WealthTitle-'].update('(%s)' %
                                       getWealthTitle(wealthValue))
    beautyValue = tryCastFloat(values['-Beauty-'])
    if event == '-Beauty-' and type(beautyValue) == float:
        window['-BeautyTitle-'].update('(%s)' %
                                       getBeautyTitle(beautyValue))
    spaceValue = tryCastFloat(values['-Space-'])
    if event == '-Space-' and type(spaceValue) == float:
        window['-SpaceTitle-'].update('(%s)' %
                                      getSpaceTitle(spaceValue))
    cleanlinessValue = tryCastFloat(values['-Cleanliness-'])
    if event == '-Cleanliness-' and type(cleanlinessValue) == float:
        window['-CleanlinessTitle-'].update('(%s)' %
                                            getCleanlinessTitle(cleanlinessValue))


def findBestUpgrade(allowSpace: bool, allowCleanliness: bool) -> any:
    stats = [scaledWealth, scaledBeauty, scaledSpace, scaledCleanliness]

    predictedWealth = scaledWealth + 0
    predictedBeauty = scaledBeauty + 0
    predictedSpace = scaledSpace + 0
    predictedCleanliness = scaledCleanliness + 0

    predictedStats = [predictedWealth, predictedBeauty,
                      predictedSpace, predictedCleanliness]
    predictedImpressiveness = calculateImpressiveness(
        predictedWealth, predictedBeauty, predictedSpace, predictedCleanliness)
    distanceToNextTitle = getDistanceToNextImpressivenessTitle(
        predictedImpressiveness)


def getDistanceToNextImpressivenessTitle(impressiveness: float) -> float or False:
    for i in range(len(impressivenessTitles)):
        if impressiveness >= impressivenessTitles[i].minValue:
            if i < len(impressivenessTitles)-1:
                nextTitleMinValue = impressivenessTitles[i+1].minValue
                return nextTitleMinValue - impressiveness
            else:
                return False


# Titles


def getValueTitle(value: float, valueType: str) -> str:
    titles = []

    match valueType:
        case 'Impressiveness':
            titles = impressivenessTitles
        case 'Wealth':
            titles = wealthTitles
        case 'Beauty':
            titles = beautyTitles
        case 'Space':
            titles = spaceTitles
        case 'Cleanliness':
            titles = cleanlinessTitles

    for title in titles:
        if (value >= title.minValue):
            return title.title

    return titles[titles.__len__ - 1]


def getImpressivenessTitle(impressiveness: int) -> str:
    return getValueTitle(impressiveness, 'Impressiveness')


def getWealthTitle(wealth: float) -> str:
    return getValueTitle(wealth, 'Wealth')


def getBeautyTitle(beauty: float) -> str:
    return getValueTitle(beauty, 'Beauty')


def getSpaceTitle(space: float) -> str:
    return getValueTitle(space, 'Space')


def getCleanlinessTitle(cleanliness: float) -> str:
    return getValueTitle(cleanliness, 'Cleanliness')

# Scaling functions


def logScaleValue(value: float) -> float:
    if value > 1:
        return 1 + math.log(value)
    elif value < -1:
        return (1+math.log(value) * -1)
    else:
        return value


def scaleWealth(wealth: float) -> float:
    return logScaleValue(wealth/1500)


def scaleBeauty(beauty: float) -> float:
    return logScaleValue(beauty/3)


def scaleSpace(space: float) -> float:
    return logScaleValue(space/125)


def scaleCleanliness(cleanliness: float) -> float:
    return logScaleValue(1 + (cleanliness / 2.5))


def tryCastFloat(input: str) -> float or False:
    try:
        return float(input)
    except ValueError:
        return False

# Calculator


def calculateImpressiveness(wealth: float, beauty: float, space: float, cleanliness: float) -> float:
    impressivenessFactors = [wealth, beauty, space, cleanliness]
    baseImpressiveness = (65 * (scaledBeauty + scaledWealth + scaledSpace +
                          scaledCleanliness) / 4) + (35 * min(impressivenessFactors))
    spaceSoftCap = math.floor(500 * space)
    if baseImpressiveness > spaceSoftCap:
        return 0.25 * baseImpressiveness + 0.75 * spaceSoftCap
    else:
        return baseImpressiveness


def setRoomImpressiveness(wealth: float, beauty: float, space: float, cleanliness: float) -> float:
    scaledWealth = scaleWealth(wealth)
    scaledBeauty = scaleBeauty(beauty)
    scaledSpace = scaleSpace(space)
    scaledCleanliness = scaleCleanliness(cleanliness)
    impressivenessFactors = [scaledBeauty,
                             scaledWealth, scaledSpace, scaledCleanliness]

    baseImpressiveness = (65 * (scaledBeauty + scaledWealth + scaledSpace +
                          scaledCleanliness) / 4) + (35 * min(impressivenessFactors))

    spaciousness = math.floor(500 * scaledSpace)
    if baseImpressiveness > spaciousness:
        roomImpressiveness = 0.25 * baseImpressiveness + 0.75 * spaciousness
    else:
        roomImpressiveness = baseImpressiveness

    roomImpressiveness = math.floor(roomImpressiveness)

    roomImpressivenessReadout.update(
        'Room impressiveness: ' + str(roomImpressiveness) + ' (' + getImpressivenessTitle(roomImpressiveness) + ')')

    spaciousnessReadout.update("Your room's impressiveness is soft-capped at: " +
                               str(spaciousness) + ' (' + getImpressivenessTitle(spaciousness) + ')' + " impressiveness due to its size.")

# Components

# Input Components


def labeledInput(label: str, key: str, initialTitle: str) -> list:
    return [sg.Text(label), sg.Input(key='-%s-' % key, enable_events=True, default_text='0'), sg.Text(text='(%s)' % initialTitle, key='-%sTitle-' % key)]


wealthInput = labeledInput(
    label='Wealth: ', key='Wealth', initialTitle=getWealthTitle(0))
beautyInput = labeledInput(
    label='Beauty: ', key='Beauty', initialTitle=getBeautyTitle(0))
spaceInput = labeledInput(label='Space: ', key='Space',
                          initialTitle=getSpaceTitle(0))
cleanlinessInput = labeledInput(
    label='Cleanliness: ', key='Cleanliness', initialTitle=getCleanlinessTitle(0))

inputSection = [sg.Column(layout=[wealthInput, beautyInput,
                          spaceInput, cleanlinessInput])]

# Readout Components

roomImpressivenessReadout = sg.Text(
    'Room impressiveness: ' + str(roomImpressiveness) + ' (' + getImpressivenessTitle(0) + ')')

spaciousnessReadout = sg.Text("Your room's impressiveness is soft-capped at: " +
                              str(spaciousness) + " impressiveness due to its size.")

# Window

window = sg.Window(title="Hello World", layout=[
    inputSection, [roomImpressivenessReadout], [spaciousnessReadout]], margins=(100, 50))

# Event Loop

while True:
    event, values = window.read()
    match event:
        case sg.WIN_CLOSED:
            break
        case '-Wealth-' | '-Beauty-' | '-Space-' | '-Cleanliness-':
            wealthValue = tryCastFloat(values['-Wealth-'])
            if event == '-Wealth-' and type(wealthValue) == float:
                window['-WealthTitle-'].update('(%s)' %
                                               getWealthTitle(wealthValue))

            beautyValue = tryCastFloat(values['-Beauty-'])
            if event == '-Beauty-' and type(beautyValue) == float:
                window['-BeautyTitle-'].update('(%s)' %
                                               getBeautyTitle(beautyValue))

            spaceValue = tryCastFloat(values['-Space-'])
            if event == '-Space-' and type(spaceValue) == float:
                window['-SpaceTitle-'].update('(%s)' %
                                              getSpaceTitle(spaceValue))

            cleanlinessValue = tryCastFloat(values['-Cleanliness-'])
            if event == '-Cleanliness-' and type(cleanlinessValue) == float:
                window['-CleanlinessTitle-'].update('(%s)' %
                                                    getCleanlinessTitle(cleanlinessValue))

            if type(wealthValue) == float and type(beautyValue) == float and type(spaceValue) == float and type(cleanlinessValue) == float:
                setRoomImpressiveness(
                    wealthValue, beautyValue, spaceValue, cleanlinessValue)
