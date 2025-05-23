import collections


class Misc:
    @staticmethod
    def toDict(layer):
        r = layer
        if isinstance(layer, collections.OrderedDict):
            r = dict(layer)

        try:
            for key, value in r.items():
                r[key] = Misc.toDict(value)
        except AttributeError:
            pass

        return r



    @staticmethod
    def deepRepr(o) -> dict:
        try:
            r = dict()

            try:
                v = vars(o)
            except TypeError:
                v = o

            if isinstance(v, dict):
                for key, val in v.items():
                    if key != "sessionUid":
                        if isinstance(val, str) or isinstance(val, int) or isinstance(val, float) or isinstance(val, bool) or not val:
                            r[key] = val

                        elif isinstance(val, list):
                            for j in val:
                                if key not in r:
                                    r[key] = list()

                                if isinstance(j, str):
                                    r[key].append(j)
                                else:
                                    r[key].append(Misc.deepRepr(j))
                        else:
                            if key not in r:
                                r[key] = dict()
                            r[key] = Misc.deepRepr(val)
        except Exception as e:
            raise e

        return r
