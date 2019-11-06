import os
import errno
import pickle
from datetime import date
from functools import partial

#borrowed from https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
def list_files(directory):
    f = []
    for (dirpath, dirnames, filenames) in os.walk(directory):
        f.extend(filenames)
        break
    f.sort()
    return f

# borrowed from https://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def is_int(n):
    return isinstance(n, int)

class Versioner():
    def __init__(self, name, obj, save_function=None, load_function=None, time_stamp=partial(date.today().strftime, "%b-%d-%Y"), version_separator='.'):
        self.full_name = name
        self.directory, self.file_name = os.path.split(name)
        self.base_name, self.file_extension = os.path.splitext(self.file_name)
        self.__make_dir()
        self.major = 1
        self.normal = 0
        self.minor = -1
        self.time_stamp = time_stamp
        self.version_separator = version_separator
        self.obj = obj
        self.save_function = save_function
        self.load_function = load_function

    def __make_dir(self):
        # check if the path is available to save
        if not os.path.isdir(self.directory):
            mkdir_p(self.directory)

    def __major_normal_minor_from_string(self, s):
        base, extension = os.path.splitext(s)
        vers = base.split(self.version_separator)
        if vers[0] != self.base_name or len(vers) < 4:
            return -1, -1, -1

        minor = int(vers.pop())
        normal = int(vers.pop())
        major = int(vers.pop())
        return major, normal, minor

    def __list_files(self):
        return list_files(self.directory)

    def __update_version(self):
        files = self.__list_files()
        if files:
            for file in files: 
                major, normal, minor = self.__major_normal_minor_from_string(file)
                if major == -1:
                    # either did not match or was wrong format
                    continue
                if not is_int(minor) or not is_int(normal) or not is_int(major):
                    raise NameError("Versions found are not ints -- minor: " + str(minor) + ", normal: " + str(normal) + ", major: " + str(major))

                if major > self.major:
                    self.major = major
                    self.normal = normal
                    self.minor = minor
                elif major == self.major and normal > self.normal:
                    self.normal = normal
                    self.minor = minor
                elif major == self.major and normal == self.normal and minor > self.minor:
                    self.minor = minor
    def __get_path(self):
        if self.time_stamp:
            save_path = f"{self.base_name}{self.version_separator}({self.time_stamp()}){self.version_separator}{self.major}{self.version_separator}{self.normal}{self.version_separator}{self.minor}{self.file_extension}"
        else:
            save_path = f"{self.base_name}{self.version_separator}{self.major}{self.version_separator}{self.normal}{self.version_separator}{self.minor}{self.file_extension}"
        return os.path.join(self.directory, save_path)

    def __commit_state(self):
        save_path = self.__get_path()
        print(f"Saving: {save_path}") 
        if not self.save_function:
            pickle.dump(self.obj, open(save_path, "wb"))
        else:
            self.save_function(self.obj, save_path)

    def __load_state(self):
        files = self.__list_files()
        if self.minor == -1:
            print("Working with initial object, NOTHING LOADED")
            return self.obj
        print(f"Attempting to load '{self.base_name}', version: {self.major}{self.version_separator}{self.normal}{self.version_separator}{self.minor}") 
        for file in files:
            major, normal, minor = self.__major_normal_minor_from_string(file)
            if major == self.major and normal == self.normal and minor == self.minor:
                path = os.path.join(self.directory, file)
                if self.load_function:
                    self.object = self.load_function(path)
                    return self.obj
                else:
                    with open(path,"rb") as f:
                        self.obj = pickle.load(f)
                    return self.obj

    def minor_increment_save(self):
        self.__update_version()
        self.minor += 1
        self.__commit_state()

    def normal_increment_save(self):
        self.__update_version()
        self.minor = 0
        self.normal += 1
        self.__commit_state()

    def major_increment_save(self):
        self.__update_version()
        self.normal = 0
        self.minor = 0
        self.major += 1
        self.__commit_state()

    def load_latest(self):
        self.__update_version()
        return self.__load_state()

    def load_specific(self, major, normal, minor):
        self.major = major
        self.normal = normal
        self.minor = minor
        return self.__load_state()
