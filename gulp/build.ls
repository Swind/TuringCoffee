require! {
    gulp
    'gulp-less': less
    'gulp-sass': sass
    'gulp-util': gutil
    'main-bower-files': bowerfiles
    'gulp-flatten': flatten
    'gulp-livescript': livescript
    'gulp-browserify': browserify
}

root_path = './src'

handleError = (err) ->
    console.error err.toString!
    @emit "end"

gulp.task 'build', ['copy-js', 'copy-css', 'copy-ls', 'copy-other', 'build-livescript', 'sass', 'browserify'] ->

gulp.task 'sass' ->
    return gulp.src "#root_path/app/scss/*.scss"
           .pipe sass!
           .pipe gulp.dest "#root_path/static/css"

gulp.task 'less' ->
    return gulp.src "#root_path/static/ls/*.less"
           .pipe less!
           .pipe gulp.dest "#root_path/static/css"

gulp.task 'build-livescript' ->
    return gulp.src "#root_path/app/ls/**/*.ls"
           .pipe livescript bare: true
           .on 'error', handleError
           .pipe gulp.dest '.tmpjs'

gulp.task 'browserify', ['build-livescript'] ->
    return gulp.src '.tmpjs/coffee.js', {base: '.tmpjs'}
    .pipe browserify {insertGlobals: true, paths: ['./node_modules', './.tmpjs']}
    .on 'error', handleError
    .pipe gulp.dest "#root_path/static/js"

gulp.task 'copy-js' ->
    return gulp.src bowerfiles ['**/*.js'], {base: './bower_components'}
           .pipe gulp.dest "#root_path/static/js"

gulp.task 'copy-ls' ->
    return gulp.src bowerfiles ['**/*.less'], {base: './bower_components'}
           .pipe gulp.dest "#root_path/static/ls"

gulp.task 'copy-css' ->
    return gulp.src bowerfiles ['**/*.css'], {base: './bower_components'}
           .pipe gulp.dest "#root_path/static/css"

others = {
    "css": ["./bower_components/bootstrap/dist/css/*.css",
            "./bower_components/bootstrap/dist/css/*.css.map",
            ]
    "js": ["./bower_components/bootstrap/dist/js/*.js",
           "./bower_components/bootstrap/dist/js/*.js.map",
           "./bower_components/codemirror/mode/markdown/*.js",
           "./bower_components/mithril/*.js.map"
           ]
    "fonts": ["./bower_components/bootstrap/dist/fonts/*.*"]
}

gulp.task 'copy-other' ->
    gulp.src others.css
        .pipe gulp.dest "#root_path/static/css"

    gulp.src others.js
        .pipe gulp.dest "#root_path/static/js"

    gulp.src others.fonts
        .pipe gulp.dest "#root_path/static/fonts"

