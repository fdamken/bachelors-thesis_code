import matplotlib.pyplot as plt
import numpy as np
import unittest
from src.orig.lds import lds



class TestPortedMatlabCode(unittest.TestCase):
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


    @unittest.skip
    def test_state2d_observation1d(self):
        # self._test(
        #        X = np.array([[1.14440269], [1.78560705], [3.12948244], [3.67578711], [2.65856131], [4.13543894], [4.3788163], [1.26264305], [0.99201493], [2.22701278]]),
        #        K = 2,
        #        expected_A = [],
        #        expected_Q = [],
        #        expected_C = [],
        #        expected_R = [],
        #        expected_x0 = [],
        #        expected_P0 = [],
        #        expected_LL = 0)
        self.fail(msg = 'This does not even work with the original code iff initialization via factor analysis is not performed.')


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


    def _test(self, X, K, expected_A, expected_Q, expected_C, expected_R, expected_x0, expected_P0, expected_LL):
        T, p = X.shape
        A, Q, C, R, x0, P0, LL, _ = lds(X, K, T, 10000, 0.00001)
        self._assertAlmostEqualMatrices(A, expected_A, 'A')
        self._assertAlmostEqualMatrices(Q, expected_Q, 'Q')
        self._assertAlmostEqualMatrices(C, expected_C, 'C')
        self._assertAlmostEqualMatrices(R, expected_R, 'R')
        self._assertAlmostEqualMatrices(x0, expected_x0, 'x0')
        self._assertAlmostEqualMatrices(P0, expected_P0, 'P0')
        self.assertAlmostEqual(LL[-1], expected_LL, places = 2)

        plt.plot(np.arange(len(LL)), LL, label = 'Log-Likelihood')
        # plt.plot(np.arange(len(ll)), ll, label = 'Log-Likelihood 2')
        plt.title('Log-Likelihood, %d Time steps' % T)
        plt.xlabel('Iteration')
        plt.ylabel('Log-Likelihood')
        plt.legend()
        plt.show()


    def _assertAlmostEqualMatrices(self, M, expected_M, matrix_name):
        regularized_M = expected_M.copy()
        regularized_M[expected_M == 0] = 1
        relative_delta = np.divide(np.abs(np.subtract(M, expected_M)), regularized_M)
        self.assertTrue((relative_delta < 0.01).all(), msg = '%s invalid! Expected %s, but was %s. Delta%%: %s' % (
                matrix_name, str(expected_M).replace('\n', ''), str(M).replace('\n', ''), str(relative_delta * 100).replace('\n', '')))



if __name__ == '__main__':
    unittest.main()
