from geo import Geo, Geos

class Experimenter:
    '''
    This class does some experiments
    '''

    def __init__(self, label):
        self.__geos = Geos()
        self.correct_dict, self.__label = self.__init_correct_dict(label)
        self.__label = label
    @property
    def geos(self):
        return self.__geos

    @property
    def label(self):
        return self.__label

    def __init_correct_dict(self, label):
        '''
        Initialize correct_dict

        Returns:
            dict{id: bool}
        '''
        self.geos.read_geos_from_database()
        correct_dict = {}
        for geo in self.geos.geos:
            correct_dict[geo.geo_id] = False
        return correct_dict, label

    def update_correct_dict(self, geo_ids, correct_flg=True):
        '''
        Args:
            geo_ids: list[int]
            correct_flg: bool
                if true update true, if false update false
        Returns:
            None
        '''
        for geo_id in geo_ids:
            try:
                self.correct_dict[geo_id] = correct_flg
            except:
                continue


    def get_value_of_dcg(self, result_list):
        '''
        Args:
            result_list[tuple(int, float)]
        Returns:
            float
        '''

        val = 0.0
        for i in range(0, len(result_list)):
            geo_id = result_list[i][0]
            if self.correct_dict[geo_id]:
                if i == 0:
                    val += result_list[i][1]
                else:
                    val += result_list[i][1] / np.log2(i + 1)
            else:
                pass
            i += 1

        return val

    def get_value_of_ap(self, result_list):
        '''
        Args:
            result_list[tuple(int, float)]
        Returns:
            float
        '''
        val = 0.0
        correct_num = 0
        for i in range(0, len(result_list)):
            geo_id = result_list[i][0]
            if self.correct_dict[geo_id]:
                correct_num += 1
                p = 1 / (i + 1)
                val += p
            else:
                pass
            i += 1

        if correct_num > 0:
            ap = val /correct_num
        else:
            ap = 0

        return ap