import re
import functools
from copy import deepcopy


def userFilters(method):
    @functools.wraps(method)
    def w(methodSelf, *methodArgs, **methodKwargs):
        try:
            # Run the wrapped method.
            o = method(methodSelf, *methodArgs, **methodKwargs)

            # Apply user filters (native REST cannot apply complex filters).
            if methodKwargs.get("userFilters"):
                for uf in methodKwargs.get("userFilters", []):
                    filteredO = []

                    # The following code covers:
                    # property eq value.
                    # property.subProperty eq value.
                    matches = re.search(r"(.*)(\ )+eq(\ )+(.*)", uf)
                    if matches:
                        k = str(matches.group(1)).strip()
                        v = str(matches.group(4)).strip()

                        for el in o:
                            if "." in k:
                                kList = k.split(".")
                                if str(el.get(kList[0], {}).get(kList[1])) == str(v):
                                    filteredO.append(el)
                            else:
                                if str(el.get(k)) == str(v):
                                    filteredO.append(el)

                    o = deepcopy(filteredO)

            return o
        except Exception as e:
            raise e

    return w
