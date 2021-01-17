//
//  ViewController.m
//  MGTestJenkins
//
//  Created by open on 2021/1/4.
//

#import "ViewController.h"

@interface ViewController ()
@property (weak, nonatomic) IBOutlet UILabel *textLbl;

@end

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // MGTestJenkinsBeta.xcworkspace
    // Do any additional setup after loading the view.
    int a = 10;
    int b = 20;
    int c = a + b;
    
    NSLog(@"输出打印内容C: %d", c);
    
    if (BETA) {
        NSLog(@"测试环境打印");
        self.textLbl.text = @"测试环境文本1.0.1分支";
    } else if (DEV) {
        NSLog(@"开发环境打印");
        self.textLbl.text = @"开发环境文本1.0.1分支";
    } else {
        NSLog(@"线上环境打印");
        self.textLbl.text = @"线上环境文本1.0.1分支";
    }
    
}


@end
