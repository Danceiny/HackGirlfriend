package com.iflytek.view;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Font;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTextArea;
import com.iflytek.cloud.speech.SpeechConstant;
import com.iflytek.cloud.speech.SpeechError;
import com.iflytek.cloud.speech.SpeechUnderstander;
import com.iflytek.cloud.speech.SpeechUnderstanderListener;
import com.iflytek.cloud.speech.TextUnderstander;
import com.iflytek.cloud.speech.TextUnderstanderListener;
import com.iflytek.cloud.speech.UnderstanderResult;
import com.iflytek.util.DebugLog;
import com.iflytek.util.DrawableUtils;

public class UnderstanderView extends JPanel implements ActionListener {
	private static final long serialVersionUID = 1L;

	private final String TEXT_UNDERSTANDER = "合肥明天的天气怎么样？";

	private JLabel labelWav;

	private JButton jbtnUnderstander;
	private JButton jbtnTextUnderstander;
	private JButton jbtnHome;

	JTextArea resultArea;

	// 语义理解对象（语音到语义）。
	private SpeechUnderstander mSpeechUnderstander;
	// 语义理解对象（文本到语义）。
	private TextUnderstander mTextUnderstander;

	/**
	 * 初始化按钮对象. 设置按钮背景图片、大小、鼠标点击事件 初始化文本框，设置字体类型、大小
	 */
	public UnderstanderView() {
		jbtnUnderstander = addButton("res/button.png", "语义理解", 0, 320, 330, -1,
				"res/button");
		ImageIcon img = new ImageIcon("res/mic_01.png");
		labelWav = new JLabel(img);
		labelWav.setBounds(0, 0, img.getIconWidth(),
				img.getIconHeight() * 4 / 5);
		jbtnUnderstander.add(labelWav, BorderLayout.WEST);

		jbtnTextUnderstander = addButton("res/button.png", "文本理解", 330, 320,
				265, -1, "res/button");
		jbtnHome = addButton("res/home.png", "", 20, 20, 1, 1, "res/home");

		resultArea = new JTextArea("");
		resultArea.setBounds(30, 100, 540, 400);
		resultArea.setOpaque(false);
		resultArea.setEditable(false);
		resultArea.setLineWrap(true);
		resultArea.setForeground(Color.BLACK);
		Font font = new Font("宋体", Font.BOLD, 21);
		resultArea.setFont(font);
		setOpaque(false);

		setLayout(null);
		add(jbtnUnderstander);
		add(jbtnTextUnderstander);
		add(resultArea);
		add(jbtnHome);

		jbtnUnderstander.addActionListener(this);
		jbtnHome.addActionListener(this);
		jbtnTextUnderstander.addActionListener(this);

		// 初始化对象
		mSpeechUnderstander = SpeechUnderstander.createUnderstander();
		mTextUnderstander = TextUnderstander.createTextUnderstander();
	}

	public JButton addButton(String imgName, String btnName, int x, int y,
			int imgWidth, int imgHeight, String iconPath) {

		JButton btn = null;
		ImageIcon img = new ImageIcon(imgName);
		btn = DrawableUtils.createImageButton(btnName, img, "center");
		int width = imgWidth, height = imgHeight;
		if (width == 1)
			width = img.getIconWidth();
		else if (width == -1)
			width = img.getIconHeight() * 4 / 5;

		if (height == 1)
			height = img.getIconWidth();
		else if (height == -1)
			height = img.getIconHeight() * 4 / 5;

		btn.setBounds(x, y, width, height);

		DrawableUtils.setMouseListener(btn, iconPath);

		return btn;
	}

	/***
	 * 监听器实现. 按钮按下动作实现
	 */
	public void actionPerformed(ActionEvent e) {

		if (e.getSource() == jbtnUnderstander) {
			resultArea.setText("");
			if (mSpeechUnderstander.isUnderstanding())
				mSpeechUnderstander.stopUnderstanding();
			// 清空Grammar_ID，防止语义理解后进行语义理解时Grammar_ID的干扰
			mSpeechUnderstander
					.setParameter(SpeechConstant.CLOUD_GRAMMAR, null);
			// 设置语义理解的引擎
			mSpeechUnderstander.setParameter(SpeechConstant.DOMAIN, "iat");
			mSpeechUnderstander.setParameter(SpeechConstant.SAMPLE_RATE,
					"16000");
			mSpeechUnderstander.setParameter(SpeechConstant.ASR_AUDIO_PATH, "./sch_test.pcm");
			if (!mSpeechUnderstander.isUnderstanding())
				mSpeechUnderstander.startUnderstanding(understanderListener);
			else
			{
				mSpeechUnderstander.stopUnderstanding();
				understanderInitUI();
			}

		} else if (e.getSource() == jbtnTextUnderstander) {
			resultArea.setText("");
			if (mTextUnderstander.isUnderstanding())
				mTextUnderstander.cancel();
			else {
				mTextUnderstander.understandText(TEXT_UNDERSTANDER,
						textListener);
			}

		} else if (e.getSource() == jbtnHome) {
			mSpeechUnderstander.cancel();
			mSpeechUnderstander.destroy();
			if (mTextUnderstander.isUnderstanding())
				mTextUnderstander.cancel();
			mTextUnderstander.destroy();

			JFrame frame = MainView.getFrame();
			frame.getContentPane().remove(this);
			JPanel panel = ((MainView) frame).getMainJpanel();
			frame.getContentPane().add(panel);
			frame.getContentPane().validate();
			frame.getContentPane().repaint();
		}

	}

	/**
	 * 语义理解回调监听器
	 */
	SpeechUnderstanderListener understanderListener = new SpeechUnderstanderListener() {
		@Override
		public void onBeginOfSpeech() {
			((JLabel) jbtnUnderstander.getComponent(0)).setText("请说话...");
		}

		@Override
		public void onError(SpeechError error) {
			if (null != error){
				DebugLog.Log("onError Code：" + error.getErrorCode());
				resultArea.setText( error.getErrorDescription(true) );
			}
			understanderInitUI();
		}

		@Override
		public void onEndOfSpeech() {
		}

		@Override
		public void onEvent(int eventType, int arg1, int arg2, String msg) {

		}

		@Override
		public void onResult(UnderstanderResult result) {
			resultArea.append(result.getResultString());
			understanderInitUI();
		}

		@Override
		public void onVolumeChanged(int volume) {
			if (volume == 0)
				volume = 1;
			else if (volume >= 6)
				volume = 6;
			labelWav.setIcon(new ImageIcon("res/mic_0" + volume + ".png"));
		}

	};
	/**
	 * 文本语义理解回调监听器
	 */
	private TextUnderstanderListener textListener = new TextUnderstanderListener() {

		@Override
		public void onResult(final UnderstanderResult result) {
			resultArea.append(result.getResultString());

		}

		@Override
		public void onError(SpeechError error) {
			if (null != error){
				DebugLog.Log("onError Code：" + error.getErrorCode());
				resultArea.setText( error.getErrorDescription(true) );
			}

		}
	};

	/**
	 * 语义理解结束，恢复初始状态
	 */
	public void understanderInitUI() {

		labelWav.setIcon(new ImageIcon("res/mic_01.png"));
		((JLabel) jbtnUnderstander.getComponent(0)).setText("语义理解");
	}
}
