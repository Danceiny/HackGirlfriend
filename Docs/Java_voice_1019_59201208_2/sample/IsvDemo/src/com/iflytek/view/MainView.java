package com.iflytek.view;

import java.awt.BorderLayout;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;

import com.iflytek.cloud.speech.SpeechUtility;
import com.iflytek.util.DrawableUtils;
import com.iflytek.util.Utils;

/**
 * MscDemo It's a Sample using MSC SDK, include tts, isr. you can just press
 * button to use it.
 * 
 */
public class MainView extends JFrame {
	private static JPanel mContentPanel;
	private static JFrame mJframe;
	private static IsvDemoView isvDemoView;
	private static LoginView loginview;

	private static final long serialVersionUID = 1L;

	/**
	 * 界面初始化.
	 * 
	 */
	public MainView() {

		// 初始化
		SpeechUtility.createUtility("appid=" + Utils.getAppid());
		// 设置界面大小，背景图片
		ImageIcon background = new ImageIcon("res/index_bg.png");
		JLabel label = new JLabel(background);
		label.setBounds(0, 0, background.getIconWidth(), background.getIconHeight());
		getLayeredPane().add(label, new Integer(Integer.MIN_VALUE));

		int frameWidth = background.getIconWidth();
		int frameHeight = background.getIconHeight();
		setSize(frameWidth, frameHeight);
		setResizable(false);
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

		isvDemoView = new IsvDemoView();
		loginview = new LoginView();

		mContentPanel = new JPanel(new BorderLayout());
		setLayout(null);
		mContentPanel.add(loginview);
		mContentPanel.setOpaque(false);

		setLocationRelativeTo(null);
		setContentPane(mContentPanel);
		setVisible(true);

	}

	public JButton addButton(String imgName, String btnName, int x, int y, int imgWidth, int imgHeight, String iconPath) {

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

	/**
	 * Demo入口函数.
	 * 
	 * @param args
	 */
	public static void main(String args[]) {
		mJframe = new MainView();
	}

	public static JFrame getFrame() {
		return mJframe;
	}

	public JButton createImageButton(ImageIcon img) {
		JButton button = new JButton("");
		button.setIcon(img);
		button.setSize(img.getIconWidth(), img.getIconHeight());
		button.setBackground(null);

		button.setBorder(null);
		button.setContentAreaFilled(false);
		button.setFocusPainted(false);

		return button;
	}

	public static void SwitchView(boolean backToLogin) {
		if (backToLogin) {
			IsvDemoView.setmAuthId("");
			loginview.setTxtUserId("");
		} else
			isvDemoView.refreshText();
		mContentPanel.remove(backToLogin ? isvDemoView : loginview);
		mContentPanel.add(backToLogin ? loginview : isvDemoView);
		mContentPanel.setOpaque(false);
		mContentPanel.validate();
		mContentPanel.repaint();
	}

	public static void setAuthId(String mAuthId) {
		if (null != isvDemoView) {
			IsvDemoView.setmAuthId(mAuthId);
		} else
			isvDemoView = new IsvDemoView();

	}

	public JPanel getContentJpanel() {
		return mContentPanel;
	}

}