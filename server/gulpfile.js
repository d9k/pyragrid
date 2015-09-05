var gulp    = require('gulp'), 
    sass    = require('gulp-ruby-sass') ,
    notify  = require('gulp-notify') ,
    bower   = require('gulp-bower'),
    coffee  = require('gulp-coffee'),
    gutil   = require('gulp-util'),
    sourcemaps = require('gulp-sourcemaps');

var config = {
    coffeePath: './best_tests_server/resources/coffee',
     sassPath: './best_tests_server/resources/sass',
     bowerDir: './bower_components' ,
    staticDir: './best_tests_server/static'
};

gulp.task('bower', function() { 
     return bower()
          .pipe(gulp.dest(config.bowerDir)) 
}); 

gulp.task('icons', function() { 
    return gulp.src(config.bowerDir + '/fontawesome/fonts/**.*') 
        .pipe(gulp.dest('./public/fonts')); 
});

gulp.task('css', function() { 
	// thx http://stackoverflow.com/questions/28140012
    return sass(config.sassPath + '/style.sass', {
            sourcemap: true,
             //style: 'compressed',
             loadPath: [
                 config.sassPath,
                 config.bowerDir + '/bootstrap-sass-official/assets/stylesheets',
                 config.bowerDir + '/fontawesome/scss'
             ]
         }) .on("error", notify.onError(function (error) {
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

// Rerun the task when a file changes
 gulp.task('watch', function() {
     gulp.watch(config.sassPath + '/**/*.scss', ['css']);
     gulp.watch(config.sassPath + '/**/*.sass', ['css']);
    gulp.watch(config.coffeePath + '/**/*.coffee', ['coffee']);
 });

  gulp.task('default', ['bower', 'icons', 'css', 'coffee']);
