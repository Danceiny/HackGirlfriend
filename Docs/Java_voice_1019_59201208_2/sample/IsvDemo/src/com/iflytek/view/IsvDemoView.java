package com.iflytek.view;

import java.awt.Color;
import java.awt.Font;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.ItemEvent;
import java.awt.event.ItemListener;
import java.io.Serializable;
import java.io.UnsupportedEncodingException;

import javax.swing.ButtonGroup;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JRadioButton;
import javax.swing.JTextArea;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import com.iflytek.cloud.speech.ErrorCode;
import com.iflytek.cloud.speech.Setting;
import com.iflytek.cloud.speech.SpeakerVerifier;
import com.iflytek.cloud.speech.SpeechConstant;
import com.iflytek.cloud.speech.SpeechError;
import com.iflytek.cloud.speech.SpeechListener;
import com.iflytek.cloud.speech.VerifierListener;
import com.iflytek.cloud.speech.VerifierResult;
import com.iflytek.util.DrawableUtils;
import com.iflytek.util.Utils;

public class IsvDemoView extends JPanel implements ActionListener, ItemListener {
	private static final long serialVersionUID = 1L;

	private JButton btnGetPassword;
	private JButton btnQueryModel;
	private JButton btnDeleteModel;
	private JButton btnRegister;
	private JButton btnCancelRegister;
	private JButton btnVerify;
	private JButton btnStopRecord;
	private JButton btnBack;

	private JTextArea txtResult;
	private JLabel txtInfo;
	private JTextArea txtShowMsg;

	private JRadioButton rdbText;
	private JRadioButton rdbFree;
	private JRadioButton rdbNumber;
	private JLabel labelWav;

	private ButtonGroup group;

	private static final int PWD_TYPE_TEXT = 1;
	private static final int PWD_TYPE_FREE = 2;
	private static final int PWD_TYPE_NUM = 3;
	// 当前声纹密码类型，1、2、3分别为文本、自由说和数字密码
	private int pwdType = PWD_TYPE_NUM;
	// 声纹识别对象
	private SpeakerVerifier mVerify;
	// 声纹AuthId
	private static String mAuthId = "";
	// 文本声纹密码
	private String mTextPwd = "";
	// 数字声纹密码
	private String mNumPwd = "";
	// 数字声纹密码段，默认有5段
	private String[] mNumPwdSegs;

	public static String getmAuthId() {
		return mAuthId;
	}

	public static void setmAuthId(String mAuthId) {
		IsvDemoView.mAuthId = mAuthId;
	}

	/**
	 * 初始化按钮对象. 设置按钮背景图片、大小、鼠标点击事件 初始化文本框，设置字体类型、大小
	 */
	public IsvDemoView() {

		//在应用发布版本中，请勿显示日志，详情见此函数说明。
		Setting.setShowLog(true);
		
		initTextArea();
		initButton();
		initRadioButton();
		setOpaque(false);
		setLayout(null);

		// 初始化SpeakerVerifier，InitListener为初始化完成后的回调接口
		mVerify = SpeakerVerifier.createVerifier();
	}

	public void initButton() {
		ImageIcon imgBtn = new ImageIcon("res/btn.png");

		btnGetPassword = DrawableUtils.createImageButton("获取密码", imgBtn, null);
		btnGetPassword.setBounds(24, 145, 120, 60);
		DrawableUtils.setMouseListener(btnGetPassword, "res/btn");
		add(btnGetPassword);
		btnGetPassword.addActionListener(this);

		btnQueryModel = DrawableUtils.createImageButton("查询模型", imgBtn, null);
		btnQueryModel.setBounds(168, 145, 120, 60);
		DrawableUtils.setMouseListener(btnQueryModel, "res/btn");
		add(btnQueryModel);
		btnQueryModel.addActionListener(this);

		btnDeleteModel = DrawableUtils.createImageButton("删除模型", imgBtn, null);
		btnDeleteModel.setBounds(312, 145, 120, 60);
		DrawableUtils.setMouseListener(btnDeleteModel, "res/btn");
		add(btnDeleteModel);
		btnDeleteModel.addActionListener(this);

		btnRegister = DrawableUtils.createImageButton("注册", imgBtn, null);
		btnRegister.setBounds(456, 145, 120, 60);
		DrawableUtils.setMouseListener(btnRegister, "res/btn");
		add(btnRegister);
		btnRegister.addActionListener(this);

		btnVerify = DrawableUtils.createImageButton("验证", imgBtn, null);
		btnVerify.setBounds(24, 220, 120, 60);
		DrawableUtils.setMouseListener(btnVerify, "res/btn");
		add(btnVerify);
		btnVerify.addActionListener(this);

		btnStopRecord = DrawableUtils.createImageButton("停止录音", imgBtn, null);
		btnStopRecord.setBounds(168, 220, 120, 60);
		DrawableUtils.setMouseListener(btnStopRecord, "res/btn");
		add(btnStopRecord);
		btnStopRecord.addActionListener(this);

		btnCancelRegister = DrawableUtils.createImageButton("取消注册", imgBtn, null);
		btnCancelRegister.setBounds(312, 220, 120, 60);
		DrawableUtils.setMouseListener(btnCancelRegister, "res/btn");
		add(btnCancelRegister);
		btnCancelRegister.addActionListener(this);

		btnBack = DrawableUtils.createImageButton("返回", imgBtn, null);
		btnBack.setBounds(456, 220, 120, 60);
		DrawableUtils.setMouseListener(btnBack, "res/btn");
		add(btnBack);
		btnBack.addActionListener(this);

	}

	public void initTextArea() {

		Font font = new Font("宋体", Font.BOLD, 18);

		txtResult = new JTextArea("");
		txtResult.setBounds(18, 10, 560, 60);
		txtResult.setLineWrap(true);
		txtResult.setOpaque(true);
		txtResult.setForeground(Color.BLACK);
		txtResult.setFont(font);
		add(txtResult);

		txtInfo = new JLabel("");
		txtInfo.setBounds(18, 80, 400, 30);
		txtInfo.setFont(font);
		add(txtInfo);

		ImageIcon img = new ImageIcon("res/mic_01.png");
		labelWav = new JLabel(img);
		labelWav.setBounds(50, 300, img.getIconWidth(), img.getIconHeight());
		add(labelWav);

		txtShowMsg = new JTextArea("");
		txtShowMsg.setBounds(240, 300, 320, 60);
		txtShowMsg.setOpaque(false);
		txtShowMsg.setEditable(false);
		txtShowMsg.setFont(font);
		add(txtShowMsg);
	}

	public void initRadioButton() {
		rdbText = new JRadioButton("文本密码");
		rdbText.setBounds(47, 105, 100, 40);
		rdbText.setOpaque(false);
		rdbText.setEnabled( false ); //文本密码正在开发中，暂不支持;
		

		rdbFree = new JRadioButton("自由说");
		rdbFree.setBounds(232, 105, 100, 40);
		rdbFree.setOpaque(false);
		rdbFree.setEnabled( false ); //自由说正在开发中，暂不支持;

		rdbNumber = new JRadioButton("数字密码");
		rdbNumber.setBounds(417, 105, 100, 40);
		rdbNumber.setOpaque(false);
		rdbNumber.setSelected(true);

		group = new ButtonGroup();
		group.add(rdbText);
		group.add(rdbFree);
		group.add(rdbNumber);

		add(rdbText);
		add(rdbFree);
		add(rdbNumber);

		rdbText.addItemListener(this);
		rdbFree.addItemListener(this);
		rdbNumber.addItemListener(this);

	}

	public void refreshText() {
		if ("" == mAuthId)
			txtInfo.setText("用户标识：匿名");
		else
			txtInfo.setText("用户标识：" + mAuthId);
	}

	public void renewUi() {
		mTextPwd = null;
		mNumPwd = null;
		txtResult.setText("");
		txtShowMsg.setText("");
		this.rdbNumber.setSelected(true);
	}

	// 执行模型操作
	private void performModelOperation(String operation, SpeechListener listener) {
		// 清空参数
		mVerify.setParameter(SpeechConstant.PARAMS, null);
		mVerify.setParameter(SpeechConstant.ISV_PWDT, "" + pwdType);

		if (pwdType == PWD_TYPE_TEXT) {
			// 文本密码删除需要传入密码
			if (Utils.isEmpty(mTextPwd)) {
				txtShowMsg.setText("请获取密码后进行操作");
				return;
			}
			mVerify.setParameter(SpeechConstant.ISV_PWD, mTextPwd);
		} else if (pwdType == PWD_TYPE_FREE) {
			mVerify.setParameter(SpeechConstant.SAMPLE_RATE, "8000");
		} else if (pwdType == PWD_TYPE_NUM) {

		}
		mVerify.sendRequest(operation, mAuthId, listener);
	}

	/***
	 * 监听器实现. 按钮按下动作实现
	 */
	public void actionPerformed(ActionEvent e) {
		// if (null == mVerify)
		// mVerify = SpeakerVerifier.createVerifier();
		if (e.getSource() == btnGetPassword) {
			// 获取密码之前要终止之前的注册过程
			mVerify.cancel();
			if (pwdType == PWD_TYPE_FREE) {
				txtResult.setText("自由说请直接注册");
				return;
			}
			// 清空参数
			mVerify.setParameter(SpeechConstant.PARAMS, null);
			Utils.Log("pwdType:" + pwdType);
			mVerify.setParameter(SpeechConstant.ISV_PWDT, "" + pwdType);
			mVerify.getPasswordList(mPwdListenter);

		} else if (e.getSource() == btnQueryModel) {
			performModelOperation("que", mModelOperationListener);
		} else if (e.getSource() == btnDeleteModel) {
			performModelOperation("del", mModelOperationListener);
		} else if (e.getSource() == btnRegister) {
			// 清空参数
			mVerify.setParameter(SpeechConstant.PARAMS, null);
			mVerify.setParameter(SpeechConstant.ISV_AUDIO_PATH, "./msc/isv_test.pcm");
			if (pwdType == PWD_TYPE_TEXT) {
				// 文本密码注册需要传入密码
				if (Utils.isEmpty(mTextPwd)) {
					txtShowMsg.setText("请获取密码后进行操作");
					return;
				}
				mVerify.setParameter(SpeechConstant.ISV_PWD, mTextPwd);
				txtShowMsg.setText("请读出：" + mTextPwd);
				txtShowMsg.append("\n训练 第" + 1 + "遍，剩余4遍");
			} else if (pwdType == PWD_TYPE_FREE) {
				txtResult.setText("请随便读一段文字，20S左右");
				mVerify.setParameter(SpeechConstant.SAMPLE_RATE, "8000");
				mVerify.setParameter(SpeechConstant.ISV_RGN, "1");
				txtShowMsg.setText("训练 第" + 1 + "遍，剩余0遍");
				mVerify.setParameter(SpeechConstant.VAD_EOS, "1800");
			} else if (pwdType == PWD_TYPE_NUM) {
				// 数字密码注册需要传入密码
				if (Utils.isEmpty(mNumPwd)) {
					txtShowMsg.setText("请获取密码后进行操作");
					return;
				}
				mVerify.setParameter(SpeechConstant.ISV_PWD, mNumPwd);
				txtShowMsg.setText("请读出：" + mNumPwd.substring(0, 8));
				txtShowMsg.append("\n训练 第" + 1 + "遍，剩余4遍");
			}

			mVerify.setParameter(SpeechConstant.ISV_AUTHID, mAuthId);
			// 设置业务类型为注册
			mVerify.setParameter(SpeechConstant.ISV_SST, "train");
			// 设置声纹密码类型
			mVerify.setParameter(SpeechConstant.ISV_PWDT, "" + pwdType);
			// 开始注册
			mVerify.startListening(mRegisterListener);
		} else if (e.getSource() == btnVerify) {
			// 清空提示信息
			txtResult.setText("");
			// 清空参数
			mVerify.setParameter(SpeechConstant.PARAMS, null);
			mVerify.setParameter(SpeechConstant.ISV_AUDIO_PATH, "./msc/verify.pcm");
			mVerify = SpeakerVerifier.getVerifier();
			// 设置业务类型为验证
			mVerify.setParameter(SpeechConstant.ISV_SST, "verify");

			if (pwdType == PWD_TYPE_TEXT) {
				// 文本密码注册需要传入密码
				if (Utils.isEmpty(mTextPwd)) {
					txtShowMsg.setText("请获取密码后进行操作");
					return;
				}
				mVerify.setParameter(SpeechConstant.ISV_PWD, mTextPwd);
				txtShowMsg.setText("请读出：" + mTextPwd);
			} else if (pwdType == PWD_TYPE_FREE) {
				txtResult.setText("请随便读一段文字，15S左右");
				mVerify.setParameter(SpeechConstant.SAMPLE_RATE, "8000");
				mVerify.setParameter(SpeechConstant.VAD_EOS, "1800");
			} else if (pwdType == PWD_TYPE_NUM) {
				// 数字密码注册需要传入密码
				String verifyPwd = mVerify.generatePassword(8);
				mVerify.setParameter(SpeechConstant.ISV_PWD, verifyPwd);
				txtShowMsg.setText("请读出：" + verifyPwd);
			}
			mVerify.setParameter(SpeechConstant.ISV_AUTHID, mAuthId);
			mVerify.setParameter(SpeechConstant.ISV_PWDT, "" + pwdType);
			// 开始验证
			mVerify.startListening(mVerifyListener);
		} else if (e.getSource() == btnStopRecord) {
			mVerify.stopListening();
			labelWav.setIcon(new ImageIcon("res/mic_01.png"));
		} else if (e.getSource() == btnCancelRegister) {
			setRadioButtonEnable( true );
			mVerify.cancel();
			txtShowMsg.setText("");
			labelWav.setIcon(new ImageIcon("res/mic_01.png"));
		} else if (e.getSource() == btnBack) {
			setRadioButtonEnable( true );
			renewUi();
			if (null != mVerify) {
				mVerify.cancel();
			}
			MainView.SwitchView(true);
		}

	}

	@Override
	public void itemStateChanged(ItemEvent evt) {
		if (evt.getStateChange() == ItemEvent.SELECTED) {
			if (evt.getSource() == rdbText) {
				pwdType = PWD_TYPE_TEXT;
			} else if (evt.getSource() == rdbFree) {
				pwdType = PWD_TYPE_FREE;
			} else if (evt.getSource() == rdbNumber) {
				pwdType = PWD_TYPE_NUM;
			}

		}
	}
	
	private void updateVolume( final int volume ){
		int idx = volume / 5 +1;	//音量值最大为30
		labelWav.setIcon( new ImageIcon("res/mic_0"+idx+".png") );
	}

	String[] items;
	SpeechListener mPwdListenter = new SpeechListener() {
		@Override
		public void onEvent(int eventType, String params) {
		}

		@Override
		public void onBufferReceived(byte[] buffer) {
			String result = null;
			try {
				result = new String(buffer, "utf-8");
			} catch (UnsupportedEncodingException e1) {
				e1.printStackTrace();
				return;
			}
			switch (pwdType) {
			case PWD_TYPE_TEXT:
				try {
					JSONObject object = new JSONObject(result);
					if (!object.has("txt_pwd")) {
						// initTextView();
						return;
					}

					JSONArray pwdArray = object.optJSONArray("txt_pwd");
					items = new String[pwdArray.length()];
					for (int i = 0; i < pwdArray.length(); i++) {
						items[i] = pwdArray.getString(i);
					}
					mTextPwd = items[0];
					txtResult.setText("您的密码：" + mTextPwd);
				} catch (JSONException e) {
					e.printStackTrace();
				}
				break;
			case PWD_TYPE_NUM:
				StringBuffer numberString = new StringBuffer();
				try {
					JSONObject object = new JSONObject(result);
					if (!object.has("num_pwd")) {
						// initTextView();
						return;
					}

					JSONArray pwdArray = object.optJSONArray("num_pwd");
					numberString.append(pwdArray.get(0));
					for (int i = 1; i < pwdArray.length(); i++) {
						numberString.append("-" + pwdArray.get(i));
					}
				} catch (JSONException e) {
					e.printStackTrace();
				}
				mNumPwd = numberString.toString();
				mNumPwdSegs = mNumPwd.split("-");
				txtResult.setText("您的密码：\n" + mNumPwd);
				break;
			default:
				break;
			}

		}

		@Override
		public void onCompleted(SpeechError error) {

			if (null != error && ErrorCode.SUCCESS != error.getErrorCode()) {
				Utils.Log("获取失败：" + error.getErrorCode());
				txtShowMsg.setText( "获取密码失败："+error.getErrorDescription(true) );
			}
		}

	};
	SpeechListener mModelOperationListener = new SpeechListener() {

		@Override
		public void onEvent(int eventType, String params) {
			// TODO Auto-generated method stub
		}

		@Override
		public void onBufferReceived(byte[] buffer) {
			String result = new String(buffer);
			try {
				JSONObject object = new JSONObject(result);
				String cmd = object.getString("cmd");
				int ret = object.getInt("ret");

				if ("del".equals(cmd)) {
					if (ret == ErrorCode.SUCCESS) {
						txtShowMsg.setText("删除成功");
					} else if (ret == ErrorCode.MSP_ERROR_FAIL) {
						txtShowMsg.setText("删除失败，模型不存在");
					}
				} else if ("que".equals(cmd)) {
					if (ret == ErrorCode.SUCCESS) {
						txtShowMsg.setText("模型存在");
					} else if (ret == ErrorCode.MSP_ERROR_FAIL) {
						txtShowMsg.setText("模型不存在");
					}
				}
			} catch (JSONException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}

		@Override
		public void onCompleted(SpeechError error) {
			if (null != error && ErrorCode.SUCCESS != error.getErrorCode()) {
				Utils.Log("操作失败：" + error.getErrorCode());
				txtShowMsg.setText( "操作失败："+error.getErrorDescription(true) );
			}
		}
	};

	VerifierListener mRegisterListener = new VerifierListener() {

		@Override
		public void onVolumeChanged(int volume) {
			Utils.Log("当前正在说话，音量大小：" + volume);
			
			updateVolume( volume );
		}

		@Override
		public void onResult(VerifierResult result) {
			Utils.Log("onResult enter:" + result.err);
			txtResult.setText( "" );
			if (result.ret == ErrorCode.SUCCESS) {
				switch (result.err) {
				case VerifierResult.MSS_ERROR_IVP_GENERAL:
					txtResult.setText("内核异常");
					break;
				case VerifierResult.MSS_ERROR_IVP_EXTRA_RGN_SOPPORT:
					txtResult.setText("训练达到最大次数");
					break;
				case VerifierResult.MSS_ERROR_IVP_TRUNCATED:
					txtResult.setText("出现截幅");
					break;
				case VerifierResult.MSS_ERROR_IVP_MUCH_NOISE:
					txtResult.setText("太多噪音");
					break;
				case VerifierResult.MSS_ERROR_IVP_UTTER_TOO_SHORT:
					txtResult.setText("录音太短");
					break;
				case VerifierResult.MSS_ERROR_IVP_TEXT_NOT_MATCH:
					txtResult.setText("您所读的文本不一致");
					break;
				case VerifierResult.MSS_ERROR_IVP_TOO_LOW:
					txtResult.setText("音量太低");
					break;
				case VerifierResult.MSS_ERROR_IVP_NO_ENOUGH_AUDIO:
					txtResult.setText("音频长达不到自由说的要求");
				default:
					txtShowMsg.setText("");
					break;
				}

				if (result.suc == result.rgn) {
					txtShowMsg.setText("注册成功");

					if (PWD_TYPE_TEXT == pwdType) {
						txtResult.setText("您的文本密码声纹ID：\n" + result.vid);
					} else if (PWD_TYPE_FREE == pwdType) {
						txtResult.setText("您的自由说声纹ID：\n" + result.vid);
					} else if (PWD_TYPE_NUM == pwdType) {
						txtResult.setText("您的数字密码声纹ID：\n" + result.vid);
					}
					
					setRadioButtonEnable( true );
					updateVolume( 0 );

				} else {
					int nowTimes = result.suc + 1;
					int leftTimes = result.rgn - nowTimes;

					if (PWD_TYPE_TEXT == pwdType) {
						txtShowMsg.setText("请读出：" + mTextPwd);
					} else if (PWD_TYPE_NUM == pwdType) {
						txtShowMsg.setText("请读出：" + mNumPwdSegs[nowTimes - 1]);
					}

					txtShowMsg.append("\n训练 第" + nowTimes + "遍，剩余" + leftTimes + "遍");
				}

			} else {
				txtShowMsg.setText("注册失败，请重新开始。");
				setRadioButtonEnable( true );
				updateVolume( 0 );
			}
		}

		@Override
		public void onError(SpeechError error) {

			if (error.getErrorCode() == ErrorCode.MSP_ERROR_ALREADY_EXIST) {
				txtShowMsg.setText("模型已存在，如需重新注册，请先删除");
			} else {
				Utils.Log("onError Code：" + error.getErrorCode());
				txtShowMsg.setText( error.getErrorDescription(true) );
			}
			
			setRadioButtonEnable( true );
			updateVolume( 0 );
		}

		@Override
		public void onEndOfSpeech() {
			Utils.Log("结束说话");
			txtShowMsg.setText( "正等待当轮结果..." );
		}

		@Override
		public void onBeginOfSpeech() {
			Utils.Log("开始说话");
			setRadioButtonEnable( false );
		}

		@Override
		public void onEvent(int arg0, int arg1, int arg2, Serializable arg3) {

		}
	};

	VerifierListener mVerifyListener = new VerifierListener() {

		@Override
		public void onVolumeChanged(int volume) {
			Utils.Log("当前正在说话，音量大小：" + volume);

			updateVolume( volume );
		}

		@Override
		public void onResult(VerifierResult result) {
			txtShowMsg.setText(result.source);

			if (result.ret == 0) {
				// 验证通过
				txtShowMsg.setText("验证通过");
			} else {
				// 验证不通过
				switch (result.err) {
				case VerifierResult.MSS_ERROR_IVP_GENERAL:
					txtShowMsg.setText("内核异常");
					break;
				case VerifierResult.MSS_ERROR_IVP_TRUNCATED:
					txtShowMsg.setText("出现截幅");
					break;
				case VerifierResult.MSS_ERROR_IVP_MUCH_NOISE:
					txtShowMsg.setText("太多噪音");
					break;
				case VerifierResult.MSS_ERROR_IVP_UTTER_TOO_SHORT:
					txtShowMsg.setText("录音太短");
					break;
				case VerifierResult.MSS_ERROR_IVP_TEXT_NOT_MATCH:
					txtShowMsg.setText("验证不通过，您所读的文本不一致");
					break;
				case VerifierResult.MSS_ERROR_IVP_TOO_LOW:
					txtShowMsg.setText("音量太低");
					break;
				case VerifierResult.MSS_ERROR_IVP_NO_ENOUGH_AUDIO:
					txtShowMsg.setText("音频长达不到自由说的要求");
					break;
				default:
					txtShowMsg.setText("验证不通过");
					break;
				}
			}
			
			setRadioButtonEnable( true );
			updateVolume( 0 );
		}

		@Override
		public void onError(SpeechError error) {

			switch (error.getErrorCode()) {
			case ErrorCode.MSP_ERROR_NOT_FOUND:
				txtShowMsg.setText("模型不存在，请先注册");
				break;
			case ErrorCode.MSP_ERROR_NET_CONNECTCLOSE:
				txtShowMsg.setText("注册失败，请重新开始。");
				break;
			default:
				Utils.Log("onError Code：" + error.getErrorCode());
				txtShowMsg.setText( error.getErrorDescription(true) );
				break;
			}
			
			setRadioButtonEnable( true );
			updateVolume( 0 );
		}

		@Override
		public void onEndOfSpeech() {
			Utils.Log("结束说话");
			txtShowMsg.setText( "正在等待结果..." );
		}

		@Override
		public void onBeginOfSpeech() {
			Utils.Log("开始说话");
			setRadioButtonEnable( false );
		}

		@Override
		public void onEvent(int arg0, int arg1, int arg2, Serializable arg3) {
			// TODO Auto-generated method stub

		}
	};

	private void setRadioButtonEnable( boolean enable ){
		this.rdbNumber.setEnabled( enable );
	}
}
