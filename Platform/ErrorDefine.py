#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


unknown_err = 100
no_err= 200

err_sys = 503
err_access_expired = 504
err_access_repeate = 505
err_user_not_login = 506
err_user_login_expired = 507
err_user_login_other = 508
err_user_id_not_exist = 511
err_user_id_existed = 512

err_password_format = 513
err_password = 514
err_article_not_exist = 515
err_user_register_error = 516
err_verifycode = 517
err_verifycode_limit = 518
err_product_is_applied = 519
err_phone_existed = 520
err_phone_is_not_used = 521
err_can_not_apply_info = 522
err_is_old_user = 523

err_no_auth = 524
err_can_not_again_apply = 525

err_query_fail = 526
err_params = 527

Message = {}
Message[unknown_err] = 'unknown error'
Message[no_err] = 'no error'
Message[err_sys] = 'system error'
Message[err_product_is_applied] = 'err_product_is_applied'
Message[err_user_id_existed] = 'err_user_id_existed'
Message[err_phone_existed] = 'err_phone_existed'
Message[err_user_id_not_exist] = 'err_user_id_not_exist'
Message[err_password] = 'err_password'
Message[err_phone_existed] = 'err_phone_existed'
Message[err_phone_is_not_used] = 'err_phone_is_not_used'
Message[err_can_not_apply_info] = 'err_can_not_apply_info'
Message[err_is_old_user] = 'err_is_old_user'
Message[err_no_auth] = 'err_no_auth'
Message[err_can_not_again_apply] = 'err_can_not_again_apply'
Message[err_query_fail] = 'err_query_fail'
Message[err_params] = 'err_params'
