import os
import glob
import shutil
from conans import ConanFile, AutoToolsBuildEnvironment, tools

class FFmpegRtspMPPConan(ConanFile):
    name = "ffmpeg_rtsp_mpp"
    version = "1.0.0"
    url = "https://gitlab.rokid-inc.com/"
    description = "A complete, cross-platform solution for face recognising and searching"
    license = ("LGPL-2.1-or-later", "GPL-2.0-or-later")
    homepage = "https://gitlab.rokid-inc.com/"
    topics = ("mpp", "streaming", "h264", "h265")
    exports_sources = ["LICENSE"]
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False],
               "fPIC": [True, False]}
    default_options = {'shared': False,
                       'fPIC': True}
    generators = "pkg_config"
    _source_subfolder = "ffmpeg_rtsp_mpp"

    def source(self):
        self.run("git clone https://github.com/ThePolarNight/ffmpeg_rtsp_mpp.git")

    def package(self):
        with tools.chdir(self._source_subfolder):
            self.copy(pattern="LICENSE")
        if self.options.shared:
            # ffmpeg produces .so files which are actually .so files
            with tools.chdir(os.path.join(self.package_folder, 'include')):
                libs = glob.glob('*.h')
                for lib in libs:
                    shutil.move(lib, lib[:-2] + '.h')
            lib_folder = os.path.join([self.package_folder, 'ffm_lib'])
            with tools.chdir(lib_folder):
                libs = glob.glob('*.so')
                for lib in libs:
                    shutil.move(lib, lib[:-2] + '.so')

    def run(self, *args, **kwargs):
        # ensure PKG_CONFIG_PATH is inherited by MSYS bash
        kwargs["with_login"] = False
        super(FFmpegRtspMPPConan, self).run(*args, **kwargs)

    def package(self):
        self.copy("ffm_inc/*.h", "include", "", keep_path=False) 
        self.copy("ffm_lib/*.*", "libs", "", keep_path=False) 
        self.copy("firefly_mpplib/*.*", "libs", "", keep_path=False)

    def package_info(self):
        includedirs = ['include']
        libdirs = ['libs']
        libs = []
        libs.extend(['avcodec-ffmpeg', 'avcodec', 'avformat-ffmpeg', 'avformat', 'avutil-ffmpeg', 'avutil'])
        if self.settings.os == "Linux":
            self.cpp_info.includedirs = includedirs
            self.cpp_info.libdirs = libdirs
            self.cpp_info.libs = libs
            self.cpp_info.system_libs.extend(['dl', 'pthread'])
