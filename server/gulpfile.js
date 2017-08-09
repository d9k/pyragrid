var gulp    = require('gulp'),
    sass    = require('gulp-ruby-sass'),
    notify  = require('gulp-notify'),
    bower   = require('gulp-bower'),
    coffee  = require('gulp-coffee'),
    gutil   = require('gulp-util'),
    sourcemaps = require('gulp-sourcemaps');

var config = {
    coffeePath: './pyragrid/resources/coffee',
    sassPath: './pyragrid/resources/sass',
//  bowerDir: './bower_components',
    nodeDir: './node_modules',
    staticDir: './pyragrid/static'
};

//gulp.task('bower', function() {
     //return bower()
         //.pipe(gulp.dest(config.bowerDir))
//}); 

gulp.task('icons', function() {
    return gulp.src(config.nodeDir + '/font-awesome/fonts/**.*')
        .pipe(gulp.dest('./public/fonts'));
});

gulp.task('css', function() {
	// thx http://stackoverflow.com/questions/28140012
    return sass(config.sassPath + '/style.sass', {
            sourcemap: true,
            //style: 'compressed',
            loadPath: [
                config.sassPath,
                config.nodeDir + '/bootstrap-sass/assets/stylesheets',
                config.nodeDir + '/font-awesome/scss'
            ]
        }).on("error", notify.onError(function (error) {
                return "Error: " + error.message;
            }))

        .pipe(sourcemaps.write(//{addComment: true, includeContent: true/*, debug: true*/}
        //TODO url prefix
        //uncomment for separate file:
        'maps', {
            includeContent: false,
            sourceRoot: 'source'
        }))
        .pipe(gulp.dest(config.staticDir + '/css'));
});

gulp.task('coffee', function(){
    gulp.src(config.coffeePath + '/**/*.coffee')
        .pipe(coffee(/*{bare: true}*/).on('error', gutil.log))
        .pipe(gulp.dest(config.staticDir + '/js'));
});

gulp.task('js-copy', function(){
    gulp.src([
            config.nodeModules + '/jquery/dist/jquery.*',
            config.nodeModules + '/jquery-ui-dist/jquery-ui.*',
            config.nodeModules + '/bootstrap-sass/assets/javascripts/bootstrap.*',
            config.nodeModules + '/datatables/media/js/jquery.dataTables.js',
            config.nodeModules + '/jqueryfiletree/dist/',
            config.nodeModules + '/lite-uploader/jquery.liteuploader*.js',
            config.nodeModules + '/blueimp-file-upload/js/jquery.fileupload.js',
            config.nodeModules + '/blueimp-file-upload/js/jquery.iframe-transport.js',
            config.nodeModules + '/blueimp-file-upload/js/vendor/jquery.ui.widget.js',
            config.nodeModules + '/blueimp-file-upload/css/jquery.fileupload.css',
            config.nodeModules + '/jinplace/js/jinplace*.js',
            config.nodeModules + '/bootstrap-confirmation2/bootstrap-confirmation*.js'
        ]).pipe(gulp.dest(config.staticDir));

    // TODO ll bower_components/blueimp-file-upload/img

    gulp.src([
        config.nodeModules + '/tinymce/**/*'
    ]).pipe(gulp.dest(config.staticDir + '/tinymce'));

    //console.log('!' + config.bowerDir + '/jqueryfiletree/dist/connectors/**/*');

    gulp.src([
        config.nodeModules + '/jqueryfiletree/dist/**/*',
        '!' + config.nodeModules + '/jqueryfiletree/dist/connectors',
    ]).pipe(gulp.dest(config.staticDir + '/jqueryfiletree'));
});


// Rerun the task when a file changes
gulp.task('watch', function() {
    //TODO try group in one array
    gulp.watch(config.sassPath + '/**/*.scss', ['css']);
    gulp.watch(config.sassPath + '/**/*.sass', ['css']);
    gulp.watch(config.coffeePath + '/**/*.coffee', ['coffee']);
 });

gulp.task('default', ['icons', 'css', 'coffee', 'js-copy']);
