import matplotlib.pyplot as plt
import numpy as np
import unittest

from src.em import EM
from src.orig.lds import lds


np.seterr(all = 'raise')



class TestLGDS(unittest.TestCase):
    def test_state3d_observation6d(self):
        self._test(
                X = np.array([[1.00638699, 1.99838508, 3.00540411, 1.00656466, 2.00155238, 3.0046599], [1.1042087, 2.19005686, 3.29688599, 1.10166544, 2.19290433, 3.3033344],
                              [1.21020251, 2.40699925, 3.64197365, 1.20919499, 2.40713648, 3.64283933], [1.33129342, 2.64952292, 4.00831707, 1.32985141, 2.64626662, 4.00449911],
                              [1.46779882, 2.89797325, 4.39713737, 1.46681058, 2.89468584, 4.39191995], [1.61270419, 3.17671326, 4.84730858, 1.61039984, 3.18014787, 4.84821803],
                              [1.77506182, 3.50745481, 5.32603554, 1.77452436, 3.50582016, 5.31945206], [1.94963315, 3.8653603, 5.86925567, 1.94782082, 3.86332969, 5.87297578],
                              [2.14733274, 4.25857648, 6.42912466, 2.14502383, 4.25201597, 6.42937554], [2.35777963, 4.69189166, 7.07105523, 2.36137592, 4.69180311, 7.06978357],
                              [2.59564077, 5.16771249, 7.76368823, 2.59761335, 5.16977797, 7.76833244], [2.85451904, 5.67435907, 8.54064727, 2.85688052, 5.68286074, 8.54170936],
                              [3.14189368, 6.24430533, 9.38485942, 3.14136922, 6.24506844, 9.3769602], [3.45498105, 6.87287846, 10.32634645, 3.44804655, 6.87761001, 10.32883726],
                              [3.79300307, 7.55484441, 11.35526366, 3.7912359, 7.56124567, 11.35213937], [4.18152861, 8.30687678, 12.48821548, 4.18308959, 8.30568581, 12.48808005],
                              [4.59349781, 9.14844123, 13.72545021, 4.59846559, 9.14788627, 13.72236064],
                              [5.06407536, 10.06482172, 15.086418, 5.06025147, 10.06024112, 15.09267422],
                              [5.56896192, 11.0670648, 16.61434133, 5.5668806, 11.06208169, 16.60553026],
                              [6.1227174, 12.17303988, 18.27245503, 6.12643891, 12.16958718, 18.28101585],
                              [6.73753092, 13.38133872, 20.0917538, 6.73750171, 13.38181507, 20.08681813],
                              [7.40549238, 14.71348653, 22.10711768, 7.40603384, 14.7146309, 22.10705615],
                              [8.14725432, 16.18536462, 24.32395372, 8.14112439, 16.17897405, 24.32224999],
                              [8.96345911, 17.8069821, 26.79225047, 8.96371367, 17.80239416, 26.79163373],
                              [9.8556342, 19.58955206, 29.45764765, 9.85754543, 19.57713262, 29.46206008],
                              [10.84209439, 21.54301134, 32.3973737, 10.84504088, 21.54100637, 32.39762278],
                              [11.93616138, 23.69686499, 35.62313509, 11.93306559, 23.69859491, 35.62203637],
                              [13.13036479, 26.05919617, 39.18489291, 13.13314736, 26.05727491, 39.18221259],
                              [14.45023293, 28.6779246, 43.0805892, 14.4531677, 28.67636788, 43.07989584],
                              [15.89595371, 31.51686469, 47.3865537, 15.8922299, 31.51941899, 47.381805],
                              [17.49101771, 34.66070659, 52.13202675, 17.49161483, 34.66191234, 52.13078619],
                              [19.24388084, 38.12699506, 57.35664877, 19.23269237, 38.13042939, 57.35176395],
                              [21.16208152, 41.93819828, 63.08560613, 21.16476951, 41.93787085, 63.08576424],
                              [23.27835484, 46.13743776, 69.39954773, 23.28290651, 46.13914312, 69.3975556],
                              [25.61247493, 50.74870034, 76.3455679, 25.61572451, 50.75196125, 76.34622155],
                              [28.17551727, 55.82822908, 83.97366587, 28.17637422, 55.82605319, 83.97997585],
                              [30.99126353, 61.40579913, 92.38366886, 30.98872135, 61.40098812, 92.38192157],
                              [34.08288426, 67.54935892, 101.61976074, 34.08371206, 67.54777515, 101.61922554],
                              [37.49555264, 74.29762732, 111.77138098, 37.49254691, 74.30153159, 111.77681494],
                              [41.24890607, 81.73468126, 122.95183909, 41.24805339, 81.73887207, 122.9492817],
                              [45.37677547, 89.92351301, 135.24478684, 45.37621378, 89.92137041, 135.24636449],
                              [49.9152001, 98.91665214, 148.78219456, 49.90818462, 98.91637718, 148.77596537],
                              [54.90670162, 108.79315205, 163.64329527, 54.90619648, 108.80034399, 163.64603858],
                              [60.40254871, 119.68742183, 179.99980571, 60.41118133, 119.68959597, 180.00249699],
                              [66.44442563, 131.65797349, 198.00139671, 66.4405279, 131.66316408, 198.00186886],
                              [73.08691248, 144.82419164, 217.8045209, 73.08297564, 144.81771355, 217.80631094],
                              [80.39660194, 159.30381675, 239.59742666, 80.40275281, 159.30563836, 239.59642586],
                              [88.43588078, 175.23634743, 263.57326548, 88.43337052, 175.23043615, 263.56346983],
                              [97.28220772, 192.76728401, 289.93679864, 97.27658685, 192.76195822, 289.94237742],
                              [107.00594227, 212.0273893, 318.93559301, 107.00709521, 212.02364662, 318.9310842]]),
                K = 3,
                expected_A = np.array([[0.211526, 0.354974, 0.060683], [-0.272793, 0.743589, 0.315028], [-0.431189, -0.400529, 1.494254]]),
                expected_Q = np.array([[0.0002956223, 0, 0], [0, 0.0000011321, 0], [0, 0, 0.0000023465]]),
                expected_C = np.array(
                        [[-0.19490, 0.22930, 0.25945], [-0.38785, 0.45547, 0.51381], [-0.58309, 0.68487, 0.77284], [-0.19492, 0.22931, 0.25944], [-0.38758, 0.45528, 0.51384],
                         [-0.58296, 0.68479, 0.77285]]),
                expected_R = np.array([0.0000414220, 0.0002574226, 0.0000080169, 0.0000485529, 0.0002638725, 0.0000110142]),
                expected_x0 = np.array([[-9.3103], [-43.7843], [-54.3536]]),
                expected_P0 = np.array([[0.130186, 0.039787, 0.062949], [0.039787, 0.012160, 0.019238], [0.062949, 0.019238, 0.030438]]),
                expected_LL = np.array(986.11))


    def test_state10d_observation6d(self):
        self._test(
                X = np.array([[1.99936483, 3.99617196, 6.02189139, 8.02292202, 9.98342, 12.00407381], [2.19870549, 4.3991568, 6.61336584, 8.79506097, 11.00042587, 13.21011533],
                              [2.42283187, 4.81772985, 7.26731931, 9.66035292, 12.11608343, 14.49409598], [2.66551089, 5.2963533, 8.01053446, 10.635214, 13.3018233, 15.94178448],
                              [2.92633834, 5.8296918, 8.81627534, 11.73058427, 14.6412957, 17.55128543], [3.22514061, 6.4119503, 9.71808479, 12.90124938, 16.08270648, 19.3089181],
                              [3.54974225, 7.04931862, 10.68994704, 14.17916327, 17.66134426, 21.24450205],
                              [3.90267209, 7.75739771, 11.76891854, 15.61759097, 19.44297926, 23.32782518],
                              [4.28758807, 8.53393249, 12.92105499, 17.19633666, 21.35645865, 25.66603652],
                              [4.71691617, 9.39617131, 14.208911, 18.90060147, 23.49142941, 28.24411572],
                              [5.18473969, 10.34328212, 15.64185833, 20.80370405, 25.85694366, 31.06239008],
                              [5.709824, 11.38398964, 17.19096443, 22.91860795, 28.44662297, 34.16574368],
                              [6.28046717, 12.51906785, 18.91084503, 25.20318886, 31.28614926, 37.59452067],
                              [6.90785717, 13.79605446, 20.81646639, 27.74482934, 34.41800743, 41.35495163],
                              [7.60335661, 15.18856502, 22.87733836, 30.51550268, 37.84473887, 45.49928348],
                              [8.34594544, 16.70527774, 25.17911252, 33.57235631, 41.63564604, 50.04605263],
                              [9.19116323, 18.36323805, 27.66171138, 36.92325478, 45.79040398, 55.02299727],
                              [10.11392436, 20.19689091, 30.42750925, 40.60992376, 50.36889319, 60.5333268],
                              [11.12139516, 22.22431187, 33.46163142, 44.66093432, 55.41357889, 66.60849385],
                              [12.23649939, 24.44408258, 36.82289063, 49.1344109, 60.97506376, 73.27840743],
                              [13.45269491, 26.8816653, 40.50627172, 54.08327054, 67.0684878, 80.59512025],
                              [14.78821722, 29.56801074, 44.56060465, 59.47973513, 73.75247958, 88.66883578],
                              [16.27438579, 32.52814083, 49.02422783, 65.40403751, 81.13527355, 97.5542319],
                              [17.91402526, 35.77817951, 53.94225392, 71.94053444, 89.27804225, 107.32962826],
                              [19.70214518, 39.35462798, 59.32870195, 79.17090843, 98.20702505, 118.09213776],
                              [21.66404207, 43.28831485, 65.25260141, 87.08612347, 108.02396273, 129.9162574],
                              [23.8363414, 47.63506123, 71.79537092, 95.79787335, 118.86424884, 142.96331134],
                              [26.2210924, 52.39170871, 78.96519408, 105.38613076, 130.78777226, 157.23695787],
                              [28.84390033, 57.62389038, 86.86683901, 115.92457846, 143.84578355, 172.95452097],
                              [31.73338527, 63.38461939, 95.55172897, 127.49836244, 158.21018694, 190.26777838],
                              [34.89818026, 69.7135891, 105.08376695, 140.2332854, 174.04002937, 209.28210852],
                              [38.38580147, 76.68794025, 115.57045314, 154.2466121, 191.44394596, 230.23527198],
                              [42.22517528, 84.34962152, 127.12038665, 169.68751564, 210.56377761, 253.25088772],
                              [46.45379228, 92.76739601, 139.83759736, 186.63855585, 231.61284303, 278.55009402],
                              [51.09009635, 102.03597992, 153.82320424, 205.30043573, 254.79786436, 306.39212514],
                              [56.20270479, 112.25685708, 169.19718351, 225.8144158, 280.26831455, 337.01139764],
                              [61.82327407, 123.47627271, 186.11036639, 248.43710206, 308.30071488, 370.71554848],
                              [68.01061055, 135.8270631, 204.72545013, 273.28804637, 339.13579243, 407.74876133],
                              [74.8054283, 149.40810539, 225.2234676, 300.61274492, 373.06417116, 448.52463739],
                              [82.28631169, 164.3465911, 247.72572278, 330.69036761, 410.3583452, 493.38098701],
                              [90.52247143, 180.79940011, 272.46653375, 363.73594999, 451.3992676, 542.73181293],
                              [99.56571064, 198.87656618, 299.70730782, 400.10814583, 496.5138419, 596.98987505],
                              [109.51691434, 218.76927182, 329.6789191, 440.12366365, 546.1539825, 656.70671431],
                              [120.47218198, 240.65061729, 362.65161142, 484.1476161, 600.75605289, 722.36218396],
                              [132.5045608, 264.73437322, 398.90880675, 532.58017728, 660.79142428, 794.64288269],
                              [145.75728079, 291.18889915, 438.78796596, 585.84608637, 726.86925328, 874.09060539],
                              [160.32790651, 320.30692594, 482.67328119, 644.4453301, 799.5287573, 961.45569931],
                              [176.36661721, 352.34777519, 530.92922091, 708.93468814, 879.48343226, 1057.61739284],
                              [193.99415549, 387.60246349, 584.03132052, 779.79940358, 967.43160168, 1163.38865981],
                              [213.39195969, 426.36021181, 642.44569635, 857.79457932, 1064.1767135, 1279.66975685]]),
                K = 10,
                expected_A = np.array([[0.4874679, -0.1203505, -0.0022180, -0.0296527, 0.0635012, 0.1086218, 0.1398700, 0.1398700, 0.1398700, 0.1398700],
                                       [-0.2455860, 0.9118421, 0.0026236, 0.0233815, -0.0951524, 0.1588326, 0.2591244, 0.2591245, 0.2591244, 0.2591244],
                                       [-0.3560860, 0.1911377, 0.6686090, 0.0559606, -0.0253538, 0.1876521, 0.3973556, 0.3973564, 0.3973554, 0.3973547],
                                       [0.1488799, -0.8175261, 0.1899452, 0.7721571, 0.2943077, 0.1212519, 0.5264748, 0.5264747, 0.5264748, 0.5264748],
                                       [-1.1401516, -0.1985248, -0.0743456, 0.1413497, 1.1351641, 0.1570816, 0.7145796, 0.7145797, 0.7145796, 0.7145796],
                                       [-1.5891125, -0.5117404, -0.0650346, 0.1711320, 0.3211076, 1.1709736, 0.8760476, 0.8760476, 0.8760476, 0.8760476],
                                       [-0.0347696, 0.0145632, -0.0090948, 0.0190563, -0.0168389, 0.0065146, 1.0042704, 0.0042704, 0.0042704, 0.0042704],
                                       [-0.0347696, 0.0145632, -0.0090947, 0.0190563, -0.0168389, 0.0065146, 0.0042704, 1.0042704, 0.0042704, 0.0042704],
                                       [-0.0347696, 0.0145632, -0.0090947, 0.0190563, -0.0168389, 0.0065146, 0.0042704, 0.0042704, 1.0042704, 0.0042704],
                                       [-0.0347696, 0.0145632, -0.0090948, 0.0190563, -0.0168389, 0.0065146, 0.0042704, 0.0042704, 0.0042704, 1.0042704]]),
                expected_Q = np.array([[7.06101098e-07, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                        0.00000000e+00, 0.00000000e+00],
                                       [0.00000000e+00, 1.05833716e-05, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                        0.00000000e+00, 0.00000000e+00],
                                       [0.00000000e+00, 0.00000000e+00, 6.04539052e-02, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                        0.00000000e+00, 0.00000000e+00],
                                       [0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 3.96073150e-05, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                        0.00000000e+00, 0.00000000e+00],
                                       [0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 1.92931074e-05, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                        0.00000000e+00, 0.00000000e+00],
                                       [0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 6.12515652e-06, 0.00000000e+00, 0.00000000e+00,
                                        0.00000000e+00, 0.00000000e+00],
                                       [0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 4.53828617e-06, 0.00000000e+00,
                                        0.00000000e+00, 0.00000000e+00],
                                       [0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 4.53828513e-06,
                                        0.00000000e+00, 0.00000000e+00],
                                       [0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                        4.53828541e-06, 0.00000000e+00],
                                       [0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                        0.00000000e+00, 4.53828541e-06]]),
                expected_C = np.array([[-0.6847417, -0.1469024, 0.0039869, 0.0812304, 0.0927270, 0.2025374, -0.0493268, -0.0493268, -0.0493268, -0.0493268],
                                       [-1.3696923, -0.2765270, -0.0088953, 0.1647666, 0.1866599, 0.4049574, -0.0986554, -0.0986554, -0.0986554, -0.0986554],
                                       [-2.0651736, -0.4240309, -0.0051290, 0.2462370, 0.2808089, 0.6104177, -0.1485663, -0.1485663, -0.1485663, -0.1485663],
                                       [-2.7554229, -0.5648030, -0.0100368, 0.3299716, 0.3755658, 0.8145575, -0.1984413, -0.1984413, -0.1984413, -0.1984413],
                                       [-3.4146260, -0.7264616, 0.0157413, 0.4065081, 0.4621314, 1.0093656, -0.2459901, -0.2459902, -0.2459900, -0.2459900],
                                       [-4.1214648, -0.7764561, -0.0705573, 0.4974171, 0.5656299, 1.2151687, -0.2963823, -0.2963822, -0.2963823, -0.2963823]]),
                expected_R = np.array([0.000015892, 0.000030514, 0.000124163, 0.000175033, 0.000071452, 0.000022059]),
                expected_x0 = np.array([[-9.7081], [-49.9861], [-81.9138], [-112.9251], [-139.6245], [-172.6500], [5.7209], [5.7209], [5.7209], [5.7209]]),
                expected_P0 = np.array([[1.35272963e-02, 6.00804592e-03, 8.52322092e-03, 1.22484975e-02, 2.43732152e-02, 3.36509429e-02, -2.07731906e-04, -2.07494447e-04,
                                         -2.07464875e-04, -2.07506094e-04],
                                        [6.00804592e-03, 4.29598353e-03, 5.92093782e-03, 8.37438405e-03, 1.13830165e-02, 1.46209505e-02, -1.21541110e-04, -1.21619239e-04,
                                         -1.21628967e-04, -1.21615382e-04],
                                        [8.52322092e-03, 5.92093782e-03, 8.63785615e-03, 1.68682035e-02, 1.45731669e-02, 1.90527441e-02, -4.57994108e-04, -4.60380477e-04,
                                         -4.60677649e-04, -4.60263027e-04],
                                        [1.22484975e-02, 8.37438405e-03, 1.68682035e-02, 9.98982753e-02, -1.54126174e-03, 3.11062484e-03, -4.69803752e-03, -4.69768187e-03,
                                         -4.69763753e-03, -4.69769937e-03],
                                        [2.43732152e-02, 1.13830165e-02, 1.45731669e-02, -1.54126173e-03, 5.17766978e-02, 6.81557903e-02, 8.62614588e-04, 8.62708666e-04,
                                         8.62720327e-04, 8.62704096e-04],
                                        [3.36509429e-02, 1.46209505e-02, 1.90527441e-02, 3.11062484e-03, 6.81557903e-02, 9.25167270e-02, 9.59193808e-04, 9.59645372e-04,
                                         9.59701608e-04, 9.59623267e-04],
                                        [-2.07731906e-04, -1.21541110e-04, -4.57994108e-04, -4.69803752e-03, 8.62614588e-04, 9.59193808e-04, 7.50252408e-01, -2.49747619e-01,
                                         -2.49747622e-01, -2.49747618e-01],
                                        [-2.07494447e-04, -1.21619239e-04, -4.60380477e-04, -4.69768187e-03, 8.62708666e-04, 9.59645372e-04, -2.49747619e-01, 7.50252354e-01,
                                         -2.49747650e-01, -2.49747645e-01],
                                        [-2.07464875e-04, -1.21628967e-04, -4.60677649e-04, -4.69763753e-03, 8.62720327e-04, 9.59701608e-04, -2.49747622e-01, -2.49747650e-01,
                                         7.50252347e-01, -2.49747649e-01],
                                        [-2.07506094e-04, -1.21615382e-04, -4.60263027e-04, -4.69769937e-03, 8.62704096e-04, 9.59623267e-04, -2.49747618e-01, -2.49747645e-01,
                                         -2.49747649e-01, 7.50252356e-01]]),
                expected_LL = 952.076,
                # A 10D state is less stable than 3D or less. Be a bit more patient.
                matrices_precision = 0.55)


    def test_state3d_observation3d(self):
        self._test(
                X = np.array([[0.00638699, -0.00117769, 1.00130776], [1.01032855, 2.0046205, 0.9990908], [2.00816343, 3.9979599, 0.99610263], [3.00146504, 5.98712799, 0.99523823],
                              [4.00138927, 7.98485319, 0.9951815], [4.99105759, 9.98741895, 0.99220059], [5.99174662, 11.97307853, 0.99240306],
                              [6.98034317, 13.95205674, 0.99052856], [7.96967405, 15.92016887, 0.99014478], [8.96138477, 17.90272298, 0.9886416],
                              [9.94262122, 19.87477107, 0.98634692], [10.9261943, 21.84063415, 0.98806541], [11.91392185, 23.81111784, 0.9739718],
                              [12.88765958, 25.75906553, 0.97258377], [13.85923589, 27.69957544, 0.97874053], [14.83458456, 29.65730874, 0.97026931],
                              [15.81071265, 31.60469313, 0.97358333], [16.78656197, 33.56242359, 0.97495556], [17.76041834, 35.50522098, 0.97612526],
                              [18.72453401, 37.44626962, 0.97060386], [19.69452415, 39.37808784, 0.97958889], [20.66689477, 41.31486174, 0.973194],
                              [21.64300611, 43.26474051, 0.96905126], [22.61488062, 45.19838116, 0.97137287], [23.57818224, 47.14916534, 0.96781657],
                              [24.55076189, 49.083292, 0.96246802], [25.52273074, 51.01023539, 0.96344874], [26.48658343, 52.93524149, 0.97000441],
                              [27.44592852, 54.85802702, 0.96227215], [28.41517313, 56.78243637, 0.96983638], [29.37531534, 58.70232496, 0.96010586],
                              [30.32834376, 60.61708528, 0.95787836], [31.29019983, 62.5221033, 0.95620396], [32.24665661, 64.4361445, 0.96018168],
                              [33.19900068, 66.34508118, 0.97066135], [34.15971909, 68.26300235, 0.96389484], [35.11696899, 70.19355956, 0.9540551],
                              [36.08228371, 72.1012632, 0.9550594], [37.03573019, 74.02028818, 0.95409737], [37.99857296, 75.93237177, 0.95244948],
                              [38.94796877, 77.82981371, 0.95029297], [39.89636053, 79.73025762, 0.95983615], [40.85719304, 81.65538338, 0.9498911],
                              [41.81206851, 83.54783476, 0.94595833], [42.75613328, 85.45114263, 0.95477331], [43.71960572, 87.35360952, 0.95949942],
                              [44.67702249, 89.27125047, 0.96035269], [45.63534219, 91.18301489, 0.96686452], [46.6058489, 93.10967018, 0.96703263],
                              [47.57385461, 95.04060515, 0.9691818]]),
                K = 3,
                expected_A = np.array([[0.7913131, 0.1072774, -0.4706017], [-0.4221447, 1.2133847, -0.5690735], [-0.0049835, 0.0061686, 0.6419861]]),
                expected_Q = np.array([[0.0000278715, 0, 0], [0, 0.0000216066, 0], [0, 0, 0.0000023456]]),
                expected_C = np.array([[0.197905951, 0.432250256, -1.272405574], [0.394887769, 0.863951395, -2.548929429], [0.000039012, -0.000474456, 0.003613186]]),
                expected_R = np.array([0.000021839, 0.000017608, 0.000041501]),
                expected_x0 = np.array([[-16.8776], [-31.4180], [5.5274]]),
                expected_P0 = np.array([[0.036605, 0.050070, 0.022655], [0.050070, 0.068495, 0.030991], [0.022655, 0.030991, 0.014022]]),
                expected_LL = 536.967)


    def test_state2d_observation2d(self):
        self._test(
                X = np.array([[0.00361892, 0.00394178], [5.98127430e-03, -1.58766809e-05], [-0.00186396, -0.00072831], [-0.00512787, -0.01305985], [-0.0057148, -0.01488854],
                              [0.00172061, -0.01739807], [-0.00370347, -0.01229228], [-0.00387223, -0.01081579], [0.00039202, -0.02889073], [-0.00596962, -0.0393046],
                              [2.30492385e-05, -4.37881928e-02], [-0.00570453, -0.0483294], [-0.00256119, -0.06920773], [-0.00282494, -0.06797544], [-0.00830006, -0.07688314],
                              [-0.01529619, -0.09292184], [-0.0106357, -0.08630195], [-0.00916236, -0.09763933], [-0.01973337, -0.10025858], [-0.01202846, -0.12131976],
                              [-0.00957165, -0.1259183], [-0.01533161, -0.13884111], [-0.02141726, -0.14755948], [-0.02735671, -0.17238522], [-0.02777585, -0.18362367],
                              [-0.03613078, -0.20636744], [-0.03309711, -0.22110595], [-0.04822117, -0.2443785], [-0.04678666, -0.25219163], [-0.04729204, -0.28347328],
                              [-0.04905907, -0.32462072], [-0.06012116, -0.34014358], [-0.06727619, -0.37515551], [-0.07487659, -0.40501297], [-0.07907032, -0.45683496],
                              [-0.0941712, -0.48938592], [-0.10108644, -0.53819774], [-0.10444969, -0.58445043], [-0.11698965, -0.64489067], [-0.1275752, -0.70182188],
                              [-0.13560718, -0.77190516], [-0.14755204, -0.83763208], [-0.16875566, -0.93534016], [-0.18190589, -1.02126296], [-0.20185475, -1.10847173],
                              [-0.22252754, -1.23267645], [-0.24026533, -1.35333695], [-0.27002782, -1.49528988], [-0.29425273, -1.65445811], [-0.32689134, -1.8238864]]),
                K = 2,
                expected_A = np.array([[1.040007, 0.022372], [0.148327, 1.060737]]),
                expected_Q = np.array([[0.00000061698, 0], [0, 0.00003410682]]),
                expected_C = np.array([[0.0082166, 0.0592152], [0.0451099, 0.3248670]]),
                expected_R = np.array([0.000016490, 0.000031421]),
                expected_x0 = np.array([[-0.64860], [1.33886]]),
                expected_P0 = np.array([[0.000000149880, -0.000000073696], [-0.000000073696, 0.000000301574]]),
                expected_LL = 382.716)


    def test_state1d_observation2d(self):
        self._test(
                X = np.array(
                        [[0.3011789, 1.90939822], [2.31946075, 4.9700876], [5.96926442, 9.10395858], [4.995872, 10.64384584], [3.28764304, 9.54745763], [3.76587575, 10.84088336],
                         [1.91679625, 9.90093096], [3.6902987, 5.17470058], [2.98179419, 4.02210119], [2.50681181, 6.29996913], [5.12481847, 4.99151513], [2.17272657, 0.29241116],
                         [-1.46654194, 0.73136154], [2.62760341, 3.40885927], [0.99387766, 0.74845933], [-0.24975245, 2.29837489], [-1.60567651, 2.23360153],
                         [-0.61426206, 1.55114132], [3.11813269, 2.41537463], [1.83228862, 4.10725191], [0.42359523, -0.19228057], [0.14355008, -0.09305687],
                         [0.31183719, -1.70331472], [-1.50861919, -1.86430733], [0.14236486, -7.8456299], [-0.78492661, -2.23891976], [-3.58910733, -1.8671838],
                         [1.81683082, -1.27939873], [-2.12620121, -1.5386451], [-1.70087938, -1.17750087], [0.55547395, -2.62164687], [-1.83230585, -4.62528505],
                         [-0.48981596, -1.71077622], [-3.19239668, -2.97640267], [-2.81002309, -3.57895583], [1.56345219, -1.96114467], [-0.84506866, -4.19312475],
                         [-0.69210414, 1.92898537], [-0.62286966, -2.14773386], [-1.08588681, -4.34077078], [-2.8694623, -1.18293771], [-2.73596975, -4.03404997],
                         [-5.76760685, -9.79255352], [-7.87173227, -11.26056334], [-6.5113265, -15.66243689], [-6.09683651, -10.43376192], [-5.57936701, -7.35564707],
                         [-4.26340758, -3.71905426], [-0.5168887, -4.9944189], [-2.75182402, -6.55992198], [-2.64575872, -7.23312114], [-2.39278708, -6.62475376],
                         [0.50145041, -2.02205863], [-0.61855155, 2.63281869], [1.237738, 6.15913572], [4.14468708, 8.64670727], [1.56914334, 4.01221113], [1.372319, 3.44517631],
                         [3.04247093, 3.76370178], [3.55398348, 11.70342966], [3.60088818, 8.11171334], [5.17938695, 12.00057128], [6.06167448, 11.13179307],
                         [3.39088513, 9.25583604], [2.56338623, 8.89516862], [3.62008479, 9.95749606], [3.33596343, 10.41072279], [7.27710237, 12.98117437],
                         [2.47083301, 8.32260567], [5.25210839, 14.49602706], [6.9370144, 12.01132637], [5.80643037, 13.57792138], [4.82443642, 9.63228931],
                         [8.54855757, 7.9095603], [3.96492984, 11.82389655], [7.87656887, 14.04716512], [7.73516735, 12.51524759], [7.14463798, 13.23887728],
                         [11.00868135, 17.36038484], [9.4399633, 21.95726417], [9.09281529, 19.22431409], [8.7819644, 20.48582353], [8.88381869, 22.11226084],
                         [8.59733719, 22.05904558], [14.84180483, 24.6146433], [14.48855099, 24.39294037], [14.4200215, 25.33816939], [8.65649772, 25.03198101],
                         [11.11852475, 28.0748915], [10.23831443, 21.90615773], [10.86828382, 27.44276105], [11.52530844, 26.48025556], [12.34604935, 26.48848346],
                         [12.81050626, 26.23633116], [13.14239951, 32.80243469], [11.9176094, 25.09653805], [11.64901834, 24.76496759], [10.99895221, 24.86639849],
                         [11.35741384, 25.94689831], [13.92148377, 26.43427591]]),
                K = 1,
                expected_A = np.array([[0.99448]]),
                expected_Q = np.array([[1.1041]]),
                expected_C = np.array([[0.99197], [2.09882]]),
                expected_R = np.array([2.0343, 2.3722]),
                expected_x0 = np.array([[-2.1986]]),
                expected_P0 = np.array([[0.0044810]]),
                expected_LL = -435.105)


    def test_state1d_observation1d(self):
        self._test(
                X = np.array([[1.18754578], [5.81828236], [1.55799504], [6.03092159], [4.86414947], [1.95417335], [-0.94046162], [-0.35895226], [0.16867977], [-4.97614568],
                              [-0.25024938], [-2.83573272], [-0.17174191], [-1.20743678], [-3.54920152], [0.39392382], [-6.13209761], [-5.3336193], [-6.69030779], [-3.7464958],
                              [-2.75915032], [-3.97918115], [-7.00645925], [-3.68448311], [-9.50460825], [-5.96507683], [-4.69356919], [-2.52085979], [-6.48151814], [-3.14023579],
                              [-6.41442181], [-10.23866896], [-3.3821397], [-4.27265451], [-7.44772334], [-2.05494684], [-2.04611725], [-7.41181601], [-9.7951435], [-13.4411126],
                              [-8.50890838], [-8.376266], [-9.48272404], [-6.33107726], [-6.66768028], [-5.51213672], [-9.40362061], [-12.49798935], [-8.2229558], [-9.32401439],
                              [-11.74168965], [-13.07971614], [-10.61037689], [-8.45602453], [-8.64862726], [-11.25500023], [-5.60255822], [-10.70829416], [-14.0449079],
                              [-8.13409547], [-10.7302329], [-9.84756427], [-0.98498105], [-8.55009886], [-8.26869612], [-9.18254811], [-9.77919903], [-8.67268743], [-13.966285],
                              [-14.84794275], [-8.85110949], [-13.63444028], [-11.93155528], [-18.38170758], [-14.02686208], [-13.56200786], [-14.77905474], [-16.48126106],
                              [-11.18579649], [-12.46197817], [-13.54851003], [-15.50508458], [-11.38455733], [-6.90363686], [-13.17743141], [-14.57419674], [-12.09618876],
                              [-10.61808991], [-9.19913943], [-6.74113855], [-13.85545703], [-12.37442405], [-12.17273562], [-13.2628806], [-17.68487873], [-13.01407894],
                              [-17.41182717], [-13.51975992], [-15.28757916], [-18.10475867]]),
                K = 1,
                expected_A = np.array([[0.96103]]),
                expected_Q = np.array([[0.65833]]),
                expected_C = np.array([[1.1845]]),
                expected_R = np.array([5.9909]),
                expected_x0 = np.array([[9.9060]]),
                expected_P0 = np.array([[0.018924]]),
                expected_LL = -248.987)


    def _test(self, X, K, expected_A, expected_Q, expected_C, expected_R, expected_x0, expected_P0, expected_LL, matrices_precision = 0.01, likelihood_precision = 0.01):
        T, p = X.shape
        em = EM(K, [X])
        A, Q, C, R, x0, P0, LL, Q_problem, R_problem, P0_problem = em.fit()
        #A, Q, C, R, x0, P0, LL, Q_problem, R_problem, P0_problem = lds(X, K, T, 10000, 0.00001)
        self.assertFalse(Q_problem, msg = 'Q problem!')
        self.assertFalse(R_problem, msg = 'R problem!')
        self.assertFalse(P0_problem, msg = 'P0 problem!')
        self.assertAlmostEqualMatrices(A, expected_A, 'A', precision = matrices_precision)
        self.assertAlmostEqualMatrices(Q, expected_Q, 'Q', precision = matrices_precision)
        self.assertAlmostEqualMatrices(C, expected_C, 'C', precision = matrices_precision)
        self.assertAlmostEqualMatrices(R, expected_R, 'R', precision = matrices_precision)
        self.assertAlmostEqualMatrices(x0, expected_x0, 'x0', precision = matrices_precision)
        self.assertAlmostEqualMatrices(P0, expected_P0, 'P0', precision = matrices_precision)
        self.assertAlmostEqualMatrices(np.array([LL[-1]]), np.array([expected_LL]), 'LL', precision = likelihood_precision)

        plt.plot(np.arange(len(LL)), LL, label = 'Log-Likelihood')
        # plt.plot(np.arange(len(ll)), ll, label = 'Log-Likelihood 2')
        plt.title('Log-Likelihood, %d Time steps' % T)
        plt.xlabel('Iteration')
        plt.ylabel('Log-Likelihood')
        plt.legend()
        plt.show()


    def assertAlmostEqualMatrices(self, M, expected_M, matrix_name, precision):
        regularized_M = expected_M.copy()
        regularized_M[expected_M == 0] = 1
        relative_delta = np.abs(np.divide(np.subtract(M, expected_M), regularized_M))
        relative_delta_old = np.divide(np.abs(np.subtract(M, expected_M)), regularized_M)
        comparison = relative_delta < precision
        to_str = lambda x: np.array_str(x, max_line_width = np.infty)
        # noinspection PyUnresolvedReferences
        self.assertTrue(comparison.all(), msg = '%s invalid! Expected:\n%s\n\nActual:\n%s\n\nRelative Delta:\n%s\n\nCorrect:\n%s\n' % (
                matrix_name, to_str(expected_M), to_str(M), to_str(relative_delta), to_str(comparison)))



if __name__ == '__main__':
    unittest.main()
