add_rules("mode.debug", "mode.release")
set_policy("package.requires_lock", true)

package("preloader")
    set_homepage("https://github.com/LiteLDev/preloader-android")
    set_description("Preloader Android SDK")
    add_urls("https://github.com/LiteLDev/preloader-android.git")
    add_versions("main", "main")
    add_deps("cmake")
    on_install("android", function (package)
        import("package.tools.cmake").install(package)
    end)
package_end()

add_requires("preloader")
add_requires("nlohmann_json v3.11.3")
add_requires("glm")
add_requires("entt")
add_requires("fmt")

target("MotionBlur")
    set_kind("shared")
    set_languages("c++20")
    set_strip("all")
    add_files("src/main.cpp",
              "src/core/**.cpp",
              "src/config/*.cpp",
              "src/launcher/*.cpp",
              "src/modules/ModuleRegistry.cpp",
              "src/modules/visual/motionblur.cpp")
    add_includedirs("include", {public = true})
    add_includedirs("src", "third_party")
    add_packages("preloader", "nlohmann_json", "glm", "entt", "fmt")
    add_defines("ENTT_PACKED_PAGE=128", "ENTT_SPARSE_PAGE=2048", {public = true})

    if is_plat("android") then
        add_cxflags("-fPIC", "-O2", "-ffunction-sections", "-fdata-sections", "-fexceptions", "-w")
        add_cxxflags("-fno-rtti")
        add_shflags("-Wl,--gc-sections", "-Wl,--hash-style=gnu", "-Wl,-z,max-page-size=16384")
        add_links("android", "log", "EGL", "GLESv3", "GLESv2")
    end
